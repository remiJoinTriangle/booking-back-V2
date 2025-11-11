from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph

from backend.serializers.hotel import HotelFilterResponse
from backend.services.agentic.nodes import WorkflowState

from .nodes import (
    database_filtering_node,
    print_query_database_node,
    reformulate_node,
    router_node,
)
from .serializers import RoutingResponse, RoutingRoute

llm = ChatOpenAI(model="gpt-4o-2024-08-06")


routing_llm = ChatOpenAI(model="gpt-4o-2024-08-06")
routing_agent = routing_llm.with_structured_output(RoutingResponse)

filter_llm = ChatOpenAI(model="gpt-4o-2024-08-06")
filter_agent = filter_llm.with_structured_output(HotelFilterResponse)
graph = StateGraph(WorkflowState)

# Add nodes
graph.add_node("router", lambda s: router_node(s, routing_agent))
graph.add_node("reformulate", lambda s: reformulate_node(s, llm))
graph.add_node("print_query_database", print_query_database_node)
from functools import partial

graph.add_node("database_filtering", partial(database_filtering_node, llm=filter_agent))


graph.add_conditional_edges(
    "router",
    lambda s: s.get("route"),
    {
        RoutingRoute.NEED_TO_PERFORM_SEARCH.value: "reformulate",
        RoutingRoute.NEED_TO_QUERY_FROM_DATABASE.value: "print_query_database",
    },
)
graph.add_edge("reformulate", END)
graph.add_edge("print_query_database", "database_filtering")
graph.add_edge("database_filtering", END)
graph.set_entry_point("router")

workflow = graph.compile()
