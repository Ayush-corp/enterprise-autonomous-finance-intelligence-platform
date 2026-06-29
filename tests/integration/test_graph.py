import pytest

from domain.graph_state import GraphState
from graph.graph import build_graph


@pytest.mark.asyncio
async def test_graph_orchestrates_analysis_with_mock_dependencies():
    workflow = build_graph()

    result = await workflow.ainvoke(GraphState(symbol="RELIANCE.NS"))
    state = GraphState.model_validate(result)

    assert state.market is not None
    assert state.news is not None
    assert state.technical is not None
    assert state.fundamental is not None
    assert state.macro is not None
    assert state.forecast is not None
    assert state.risk is not None
    assert state.reflection is not None
    assert state.recommendation is not None
