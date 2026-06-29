from agents.committee.agent import CommitteeAgent
from agents.committee.models import CommitteeAgentInput
from domain.graph_state import GraphState


async def committee_node(
    state: GraphState,
    agent: CommitteeAgent,
) -> GraphState:

    result = await agent.run(
        CommitteeAgentInput(
            symbol=state.symbol,
            forecast=state.forecast,
            risk=state.risk,
            reflection=state.reflection,
        )
    )

    state.committee = result

    return state