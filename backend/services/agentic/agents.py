from langchain_openai import ChatOpenAI

from backend.services.agentic.serializers import (
    HotelFilterResponse,
    RankingResponse,
    RoutingResponse,
)

# MARK: DEFINITION OF THE LLMS with strucutured outputs

routing_llm = ChatOpenAI(model="gpt-4o-2024-08-06")
routing_agent = routing_llm.with_structured_output(RoutingResponse)

filter_llm = ChatOpenAI(model="gpt-4o-2024-08-06")
filter_agent = filter_llm.with_structured_output(HotelFilterResponse)

ranking_llm = ChatOpenAI(model="gpt-4o-2024-08-06")
ranking_agent = ranking_llm.with_structured_output(RankingResponse)
