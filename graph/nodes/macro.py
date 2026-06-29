from agents.macro.agent import MacroAgent
from agents.macro.models import MacroAgentInput
from domain.graph_state import GraphState


async def macro_node(
    state: GraphState,
    agent: MacroAgent,
) -> GraphState:

    result = await agent.run(
        MacroAgentInput(
            symbol=state.symbol,
        )
    )

    state.macro = result

    return state