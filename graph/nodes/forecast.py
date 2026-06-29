from agents.forecast.agent import ForecastAgent
from agents.forecast.models import ForecastAgentInput
from domain.graph_state import GraphState


async def forecast_node(
    state: GraphState,
    agent: ForecastAgent,
) -> GraphState:

    result = await agent.run(
        ForecastAgentInput(
            symbol=state.symbol,
            news=state.news,
            technical=state.technical,
            fundamental=state.fundamental,
            macro=state.macro,
        )
    )

    state.forecast = result

    return state