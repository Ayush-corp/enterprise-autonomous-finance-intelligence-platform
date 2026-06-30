from langgraph.graph import END, START, StateGraph

from app.dependencies.services import get_llm_service, get_market_provider, get_news_provider
from domain.forecast import Forecast
from domain.fundamental import FundamentalAnalysis
from domain.graph_state import GraphState
from domain.macro import MacroAnalysis
from domain.recommendation import Recommendation
from domain.reflection import ReflectionAnalysis
from domain.risk import RiskAssessment
from domain.technical import TechnicalAnalysis
from app.core.exceptions import InvalidGraphStateError


def coerce_state(state: GraphState | dict[str, object]) -> GraphState:
    if isinstance(state, GraphState):
        return state
    return GraphState.model_validate(state)


def require_fields(state: GraphState, *fields: str) -> None:
    missing = [field for field in fields if getattr(state, field) is None]
    if missing:
        raise InvalidGraphStateError(f"Graph state missing required field(s): {', '.join(missing)}")


def _prompt(state: GraphState, task: str) -> str:
    return f"Symbol: {state.symbol}\n\nTask: {task}\n\nState:\n{state.model_dump_json(indent=2)}"


def build_graph():
    llm_service = get_llm_service()
    market_provider = get_market_provider()
    news_provider = get_news_provider()
    builder = StateGraph(GraphState)

    async def market_node(state):
        graph_state = coerce_state(state)
        return {"market": await market_provider.get_snapshot(graph_state.symbol)}

    async def news_node(state):
        graph_state = coerce_state(state)
        return {"news": await news_provider.analyze(graph_state.symbol)}

    async def technical_node(state):
        graph_state = coerce_state(state)
        require_fields(graph_state, "market")
        result = await llm_service.structured(
            "You are a technical analyst.",
            _prompt(graph_state, "Produce technical analysis."),
            TechnicalAnalysis,
        )
        return {"technical": result.structured}

    async def fundamental_node(state):
        graph_state = coerce_state(state)
        result = await llm_service.structured(
            "You are a fundamental analyst.",
            _prompt(graph_state, "Produce fundamental analysis."),
            FundamentalAnalysis,
        )
        return {"fundamental": result.structured}

    async def macro_node(state):
        graph_state = coerce_state(state)
        result = await llm_service.structured(
            "You are a macro analyst.",
            _prompt(graph_state, "Produce macro analysis."),
            MacroAnalysis,
        )
        return {"macro": result.structured}

    async def forecast_node(state):
        graph_state = coerce_state(state)
        require_fields(graph_state, "market", "news", "technical", "fundamental", "macro")
        result = await llm_service.structured(
            "You forecast short-term equity direction.",
            _prompt(graph_state, "Produce a forecast."),
            Forecast,
        )
        return {"forecast": result.structured}

    async def risk_node(state):
        graph_state = coerce_state(state)
        require_fields(graph_state, "forecast")
        result = await llm_service.structured(
            "You assess investment risk.",
            _prompt(graph_state, "Produce a risk assessment."),
            RiskAssessment,
        )
        return {"risk": result.structured}

    async def reflection_node(state):
        graph_state = coerce_state(state)
        require_fields(graph_state, "forecast", "risk")
        result = await llm_service.structured(
            "You critique investment analysis.",
            _prompt(graph_state, "Produce reflection analysis."),
            ReflectionAnalysis,
        )
        return {"reflection": result.structured}

    async def committee_node(state):
        graph_state = coerce_state(state)
        require_fields(graph_state, "forecast", "risk", "reflection")
        result = await llm_service.structured(
            "You are an investment committee.",
            _prompt(graph_state, "Produce a final recommendation."),
            Recommendation,
        )
        return {"recommendation": result.structured}

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
