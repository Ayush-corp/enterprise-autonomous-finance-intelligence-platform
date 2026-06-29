from collections.abc import Awaitable, Callable

from app.core.exceptions import InvalidGraphStateError
from domain.graph_state import GraphState


GraphNode = Callable[[GraphState], Awaitable[dict[str, object]]]


def coerce_state(state: GraphState | dict[str, object]) -> GraphState:
    if isinstance(state, GraphState):
        return state
    return GraphState.model_validate(state)


def require_fields(state: GraphState, *fields: str) -> None:
    missing = [field for field in fields if getattr(state, field) is None]
    if missing:
        raise InvalidGraphStateError(f"Graph state missing required field(s): {', '.join(missing)}")
