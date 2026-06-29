from agents.technical.agent import TechnicalAgent
from agents.technical.models import TechnicalAgentInput
from domain.graph_state import GraphState


async def technical_node(
    state: GraphState,
    agent: TechnicalAgent,
) -> GraphState:

    result = await agent.run(
        TechnicalAgentInput(
            symbol=state.symbol,
        )
    )

    state.technical = result

    return state