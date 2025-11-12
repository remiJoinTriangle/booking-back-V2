from langgraph.graph import END, StateGraph

from backend.services.agentic.nodes import WorkflowState

from .nodes import (
    database_filtering_node,
    external_search_node,
    ranking_node,
    router_node,
)
from .serializers import RoutingRoute

# MARK: DEFINITION OF THE GRAPH

graph = StateGraph(WorkflowState)

# Add nodes
graph.add_node("router", router_node)
graph.add_node("external_search", external_search_node)
graph.add_node("ranking", ranking_node)
graph.add_node("database_filtering", database_filtering_node)

# MARK: ADD CONDITIONAL EDGES

# add conditional edges based on the route
graph.add_conditional_edges(
    "router",
    lambda s: s.route,
    {
        RoutingRoute.NEED_TO_EXTERNAL_SEARCH.value: "external_search",
        RoutingRoute.NEED_TO_QUERY_FROM_DATABASE.value: "database_filtering",
    },
)

# MARK: ADD EDGES BETWEEN NODES
graph.add_edge("external_search", END)


graph.add_edge("database_filtering", "ranking")
graph.add_edge("ranking", END)


graph.set_entry_point("router")

# MARK: COMPILE THE GRAPH
workflow = graph.compile()
