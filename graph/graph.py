from dataclasses import dataclass

from langgraph.graph import END, START, StateGraph

from agents.committee_agent import CommitteeAgent
from agents.forecast_agent import ForecastAgent
from agents.fundamental_agent import FundamentalAgent
from agents.macro_agent import MacroAgent
from agents.market_agent import MarketAgent
from agents.news_agent import NewsAgent
from agents.reflection_agent import ReflectionAgent
from agents.risk_agent import RiskAgent
from agents.technical_agent import TechnicalAgent
from app.dependencies.services import get_llm_service, get_market_provider, get_news_provider
from domain.graph_state import GraphState
from graph.nodes import coerce_state, require_fields


@dataclass(frozen=True)
class AgentBundle:
    market: MarketAgent
    news: NewsAgent
    technical: TechnicalAgent
    fundamental: FundamentalAgent
    macro: MacroAgent
    forecast: ForecastAgent
    risk: RiskAgent
    reflection: ReflectionAgent
    committee: CommitteeAgent


def default_agents() -> AgentBundle:
    llm_service = get_llm_service()
    return AgentBundle(
        market=MarketAgent(get_market_provider()),
        news=NewsAgent(get_news_provider()),
        technical=TechnicalAgent(llm_service),
        fundamental=FundamentalAgent(llm_service),
        macro=MacroAgent(llm_service),
        forecast=ForecastAgent(llm_service),
        risk=RiskAgent(llm_service),
        reflection=ReflectionAgent(llm_service),
        committee=CommitteeAgent(llm_service),
    )


def build_graph(agents: AgentBundle | None = None):
    agent_bundle = agents or default_agents()
    builder = StateGraph(GraphState)

    async def market_node(state):
        graph_state = coerce_state(state)
        return {"market": await agent_bundle.market.run(graph_state.symbol)}

    async def news_node(state):
        graph_state = coerce_state(state)
        return {"news": await agent_bundle.news.run(graph_state.symbol)}

    async def technical_node(state):
        graph_state = coerce_state(state)
        require_fields(graph_state, "market")
        return {"technical": await agent_bundle.technical.run(graph_state)}

    async def fundamental_node(state):
        graph_state = coerce_state(state)
        return {"fundamental": await agent_bundle.fundamental.run(graph_state)}

    async def macro_node(state):
        graph_state = coerce_state(state)
        return {"macro": await agent_bundle.macro.run(graph_state)}

    async def forecast_node(state):
        graph_state = coerce_state(state)
        require_fields(graph_state, "market", "news", "technical", "fundamental", "macro")
        return {"forecast": await agent_bundle.forecast.run(graph_state)}

    async def risk_node(state):
        graph_state = coerce_state(state)
        require_fields(graph_state, "forecast")
        return {"risk": await agent_bundle.risk.run(graph_state)}

    async def reflection_node(state):
        graph_state = coerce_state(state)
        require_fields(graph_state, "forecast", "risk")
        return {"reflection": await agent_bundle.reflection.run(graph_state)}

    async def committee_node(state):
        graph_state = coerce_state(state)
        require_fields(graph_state, "forecast", "risk", "reflection")
        return {"recommendation": await agent_bundle.committee.run(graph_state)}

    builder.add_node("market", market_node)
    builder.add_node("news", news_node)
    builder.add_node("technical", technical_node)
    builder.add_node("fundamental", fundamental_node)
    builder.add_node("macro", macro_node)
    builder.add_node("forecast", forecast_node)
    builder.add_node("risk", risk_node)
    builder.add_node("reflection", reflection_node)
    builder.add_node("committee", committee_node)

    builder.add_edge(START, "market")
    builder.add_edge("market", "news")
    builder.add_edge("market", "technical")
    builder.add_edge("market", "fundamental")
    builder.add_edge("market", "macro")
    builder.add_edge(["news", "technical", "fundamental", "macro"], "forecast")
    builder.add_edge("forecast", "risk")
    builder.add_edge("risk", "reflection")
    builder.add_edge("reflection", "committee")
    builder.add_edge("committee", END)

    return builder.compile()


graph = build_graph()
