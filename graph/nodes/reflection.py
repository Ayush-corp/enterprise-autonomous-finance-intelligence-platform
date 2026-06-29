from agents.reflection.agent import ReflectionAgent
from agents.reflection.models import ReflectionAgentInput
from domain.graph_state import GraphState


async def reflection_node(
    state: GraphState,
    agent: ReflectionAgent,
) -> GraphState:

    result = await agent.run(
        ReflectionAgentInput(
            symbol=state.symbol,
            forecast=state.forecast,
            risk=state.risk,
        )
    )

    state.reflection = result

    return state