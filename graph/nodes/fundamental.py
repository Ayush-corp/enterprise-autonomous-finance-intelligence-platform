from agents.fundamental.agent import FundamentalAgent
from agents.fundamental.models import FundamentalAgentInput
from domain.graph_state import GraphState


async def fundamental_node(
    state: GraphState,
    agent: FundamentalAgent,
) -> GraphState:

    result = await agent.run(
        FundamentalAgentInput(
            symbol=state.symbol,
        )
    )

    state.fundamental = result

    return state