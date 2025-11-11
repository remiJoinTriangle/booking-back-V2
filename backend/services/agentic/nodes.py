from typing import Any, Dict, List, Optional, TypedDict

from langchain_openai import ChatOpenAI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import AsyncSessionLocal
from backend.models import Hotel
from backend.serializers.hotel import HotelFilter, HotelFilterResponse, HotelResponse
from backend.services.hotel_service import apply_filters


class WorkflowState(TypedDict, total=False):
    """State passed between graph nodes."""

    input: Optional[str]
    route: str
    reformulated: str
    action: str
    result: str
    filters: HotelFilterResponse
    hotels: Optional[List[HotelResponse]]


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


def router_node(state: WorkflowState, llm: Any) -> Dict[str, str]:
    """Decide whether to follow branch A or B."""
    prompt = (
        """You are a classifier. Decide whether the input is case: 
        - SEARCH:Need to perform a search (web/api) to clarify the user's request. If the user's request is not clear, use this route. If the user's request contextual data, use this route.
        - QUERY_DATABASE: Need to query from our existing database to answer the user's request. Whenever a user asks for a list of Hotels or query for a particular hotel use this route.
        """
        f"Input: {state['input']}"
    )
    response = llm.invoke(prompt)
    print(response.route.value)

    return {"route": response.route.value}


def reformulate_node(state: WorkflowState, llm: ChatOpenAI) -> Dict[str, str]:
    """Reformulate the input text."""
    prompt = f"Reformulate the following text more clearly:\n{state['input']}"
    reformulated = _to_text(llm.invoke(prompt).content)
    return {"reformulated": reformulated, "action": "I've reformulated the input"}


async def database_filtering_node(state: WorkflowState, llm: Any) -> Dict[str, Any]:
    prompt = f"""I need to filter a query to get the hotels that match the following criteria from the user::\n{state["input"]}"""
    response = await llm.ainvoke(prompt)
    filters: HotelFilter = response.filter
    query = select(Hotel)
    query = apply_filters(query, filters)
    async with AsyncSessionLocal() as db:
        result = await db.execute(query.limit(10))
        hotels = result.scalars().all()
        formatted_hotels = [HotelResponse.from_orm(hotel) for hotel in hotels]
        return {
            "hotels": formatted_hotels,
            "filters": filters,
            "action": "I've filtered the database",
        }


def print_query_database_node(state: WorkflowState) -> Dict[str, str]:
    """Print the query to the database."""
    return {"action": "I've queries db"}
