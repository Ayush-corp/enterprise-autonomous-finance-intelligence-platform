from langgraph.graph import END, START, StateGraph

from app.dependencies.services import get_llm_service, get_market_provider, get_news_provider
from domain.analysis import AnalysisSynthesis
from domain.graph_state import GraphState
from domain.technical import TechnicalAnalysis
from graph.nodes import coerce_state, require_fields


def _technical_from_market(state: GraphState) -> TechnicalAnalysis:
    require_fields(state, "market")
    market = state.market
    assert market is not None

    price_gap_pct = ((market.current_price - market.sma20) / market.sma20) * 100
    if price_gap_pct > 1:
        momentum = "positive"
    elif price_gap_pct < -1:
        momentum = "negative"
    else:
        momentum = "neutral"

    support = min(market.current_price, market.sma20) * 0.98
    resistance = max(market.current_price, market.sma20) * 1.02
    confidence = min(0.85, max(0.45, 0.55 + abs(price_gap_pct) / 25))

    return TechnicalAnalysis(
        symbol=market.symbol,
        trend=market.trend.value if hasattr(market.trend, "value") else str(market.trend),
        momentum=momentum,
        support=round(support, 2),
        resistance=round(resistance, 2),
        confidence=round(confidence, 2),
        summary=(
            f"{market.symbol} trades at {market.current_price:.2f} versus a 20-day SMA of "
            f"{market.sma20:.2f}. The deterministic technical read is {market.trend} "
            f"with {momentum} momentum."
        ),
    )


def _synthesis_prompt(state: GraphState) -> str:
    return (
        "Produce an investment analysis for the requested horizon using only the supplied "
        "market, news, and deterministic technical context.\n\n"
        f"State:\n{state.model_dump_json(indent=2)}"
    )


def build_graph():
    llm_service = get_llm_service()
    market_provider = get_market_provider()
    news_provider = get_news_provider()
    builder = StateGraph(GraphState)

    async def market_node(state):
        graph_state = coerce_state(state)
        return {
            "market": await market_provider.get_snapshot(
                graph_state.symbol,
                graph_state.country,
            )
        }

    async def news_node(state):
        graph_state = coerce_state(state)
        return {"news": await news_provider.analyze(graph_state.symbol)}

    async def technical_node(state):
        graph_state = coerce_state(state)
        return {"technical": _technical_from_market(graph_state)}

    async def synthesis_node(state):
        graph_state = coerce_state(state)
        require_fields(graph_state, "market", "news", "technical")
        result = await llm_service.structured(
            "You are InvestorOS, an Indian-market investment intelligence engine. "
            "Return conservative, structured, research-only output. This is not financial advice.",
            _synthesis_prompt(graph_state),
            AnalysisSynthesis,
        )
        if result.structured is None:
            raise ValueError("LLM provider returned no analysis synthesis")
        synthesis = result.structured
        return {
            "fundamental": synthesis.fundamental,
            "macro": synthesis.macro,
            "forecast": synthesis.forecast,
            "risk": synthesis.risk,
            "reflection": synthesis.reflection,
            "recommendation": synthesis.recommendation,
        }

    builder.add_node("market", market_node)
    builder.add_node("news", news_node)
    builder.add_node("technical", technical_node)
    builder.add_node("synthesis", synthesis_node)

    builder.add_edge(START, "market")
    builder.add_edge("market", "news")
    builder.add_edge("market", "technical")
    builder.add_edge(["news", "technical"], "synthesis")
    builder.add_edge("synthesis", END)

    return builder.compile()


graph = build_graph()
