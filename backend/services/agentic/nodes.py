import os
from typing import Any, Dict, List, Optional

from openai import AsyncOpenAI
from pydantic import BaseModel
from sqlalchemy import select

from backend.database import AsyncSessionLocal
from backend.models import Hotel
from backend.serializers.hotel import HotelResponse
from backend.serializers.session import MessageResponse
from backend.services.agentic.serializers import (
    HotelFilter,
    HotelFilterResponse,
    RoutingResponse,
)
from backend.services.hotel_service import apply_filters

from .agents import filter_agent, ranking_agent, routing_agent


class WorkflowState(BaseModel):
    """State passed between graph nodes."""

    input: Optional[str] = None
    previous_messages: Optional[List[MessageResponse]] = None
    route: Optional[str] = None
    reformulated: Optional[str] = None
    action: Optional[str] = None
    result: Optional[str] = None
    filters: Optional[HotelFilterResponse] = None
    hotels: Optional[List[HotelResponse]] = None
    external_search: Optional[str] = None
    ranking_ids: Optional[List[int]] = None
    ranked_hotels: Optional[List[HotelResponse]] = None

    @property
    def previous_messages_json(self) -> List[Dict[str, str]]:
        if self.previous_messages is None:
            return []
        return [p.to_dict() for p in self.previous_messages]


def _to_text(content: Any) -> str:
    if isinstance(content, str):
        return content.strip()
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(item.get("text", ""))
        return "".join(parts).strip()
    return str(content).strip()


def router_node(state: WorkflowState) -> Dict[str, str]:
    """Decide whether to follow branch A or B."""
    prompt = (
        """You are a classifier. Decide whether the input is case: 
        - SEARCH:Need to perform a search (web/api) when you think it's not related to a db query (like current weather, festivals, etc).
        - QUERY_DATABASE: Need to query from our existing database to answer the user's request. Whenever a user asks for a list of Hotels or query for a particular hotel use this route.
        """
        f"Input: {state.input}"
        "Take into account the previous messages to decide the next action. Assume that some follow up question are asked to refine the DB query."
        f"Previous messages: {state.previous_messages_json}"
    )
    response: RoutingResponse = routing_agent.invoke(prompt)  # type: ignore

    return {"route": response.route.value}


client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])


async def external_search_node(state: WorkflowState) -> Dict[str, str]:
    prompt = f"""
    Perform an external search for the following query:\n{state.input}
    Take chat history into account to perform the search the best way possible.
    Chat history: {state.previous_messages_json}
    """

    response = await client.responses.create(
        model="gpt-4.1",  # ou gpt-4o-mini, selon ton usage
        input=prompt,
        tools=[{"type": "web_search"}],
    )

    external_search = response.output_text

    return {
        "external_search": external_search,
        "action": "I've performed an external search",
    }


async def database_filtering_node(state: WorkflowState) -> Dict[str, Any]:
    prompt = f"""
    I need to filter a query to get the hotels that match the following criteria from the user::\n{state.input}
    but also take into account the previous messages to refine the query.
    Previous messages: {state.previous_messages_json}
    """
    response = await filter_agent.ainvoke(prompt)
    filters: HotelFilter = response.filter  # type: ignore
    query = select(Hotel)
    query = apply_filters(query, filters)
    async with AsyncSessionLocal() as db:
        result = await db.execute(query.limit(10))
        hotels = result.scalars().all()
        formatted_hotels = [HotelResponse.from_orm(hotel) for hotel in hotels]
        return {
            "hotels": formatted_hotels,
            "filters": response,
            "action": "I've filtered the database",
        }


async def ranking_node(state: WorkflowState) -> Dict[str, Any]:
    prompt = f"""
    Rank the following hotels by their relevance to the user's request:
    Use this kind of formula to rank the hotels:
    score = commentAggregatedRating*100+starRating*50-price*80(the lower the better) +vibes*20+flag*10+vibeFlag*10(the higher the better)
    Sort the hotels by their score in descending order.
    {state.input}
    Hotels: {[hotel.model_dump() for hotel in state.hotels] if state.hotels else []}
    Previous messages: {state.previous_messages_json}
    """
    response = await ranking_agent.ainvoke(prompt)
    ranked_hotels_ids = response.desc_sorted_hotels_ids  # type: ignore
    hotels_mapping = {hotel.id: hotel for hotel in state.hotels}  # type: ignore
    hotels = [hotels_mapping.get(hotel_id) for hotel_id in ranked_hotels_ids]
    return {
        "ranking_ids": ranked_hotels_ids,
        "action": "I've ranked the hotels",
        "ranked_hotels": hotels,
    }
