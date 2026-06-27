from langgraph.graph import StateGraph
from graph.state import AgentState

from agents.market_agent import market_agent
from agents.news_agent import news_agent
from agents.fundamental_agent import fundamental_agent
from agents.technical_agent import technical_agent
from agents.forecast_agent import forecast_agent
from agents.risk_agent import risk_agent
from agents.decision_agent import decision_agent


def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("market", market_agent)
    workflow.add_node("news", news_agent)
    workflow.add_node("fundamental", fundamental_agent)
    workflow.add_node("technical", technical_agent)
    workflow.add_node("forecast", forecast_agent)
    workflow.add_node("risk", risk_agent)
    workflow.add_node("decision", decision_agent)

    workflow.set_entry_point("market")

    workflow.add_edge("market", "news")
    workflow.add_edge("news", "fundamental")
    workflow.add_edge("fundamental", "technical")
    workflow.add_edge("technical", "forecast")
    workflow.add_edge("forecast", "risk")
    workflow.add_edge("risk", "decision")

    workflow.set_finish_point("decision")

    return workflow.compile()


graph = build_graph()