from langgraph.graph import StateGraph
from langgraph.graph import END

from graph.state import GraphState
from graph.nodes import *

builder = StateGraph(GraphState)

builder.add_node("market", market_node)

builder.add_node("news", news_node)

builder.add_node("decision", decision_node)

builder.set_entry_point("market")

builder.add_edge("market", "news")

builder.add_edge("news", "decision")

builder.add_edge("decision", END)

graph = builder.compile()