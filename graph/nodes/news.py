from agents.news.agent import NewsAgent
from agents.news.models import NewsAgentInput
from domain.graph_state import GraphState


async def news_node(
    state: GraphState,
    agent: NewsAgent,
) -> GraphState:

    result = await agent.run(
        NewsAgentInput(
            symbol=state.symbol,
        )
    )

    state.news = result

    return state