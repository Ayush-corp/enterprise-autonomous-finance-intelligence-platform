from agents.market.agent import MarketAgent
from agents.market.models import MarketAgentInput
from domain.graph_state import GraphState


async def market_node(
    state: GraphState,
    agent: MarketAgent,
) -> GraphState:

    result = await agent.run(
        MarketAgentInput(
            symbol=state.symbol,
        )
    )

    state.market = result

    return state