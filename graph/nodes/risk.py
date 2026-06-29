from agents.risk.agent import RiskAgent
from agents.risk.models import RiskAgentInput
from domain.graph_state import GraphState


async def risk_node(
    state: GraphState,
    agent: RiskAgent,
) -> GraphState:

    result = await agent.run(
        RiskAgentInput(
            symbol=state.symbol,
            forecast=state.forecast,
        )
    )

    state.risk = result

    return state