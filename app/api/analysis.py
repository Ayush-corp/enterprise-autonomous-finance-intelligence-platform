from uuid import uuid4

import structlog
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.core.exceptions import ExternalProviderError, InvestorOSError, LLMProviderError
from domain.graph_state import GraphState
from domain.prediction import PredictionHorizon
from graph.graph import graph


router = APIRouter(prefix="/api/v1", tags=["Analysis"])
logger = structlog.get_logger(__name__)


class AnalysisRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=32)
    country: str | None = Field(default=None, min_length=2, max_length=2)
    horizon: PredictionHorizon = PredictionHorizon.SEVEN_DAYS


@router.post("/analyze", response_model=GraphState)
async def analyze(request: AnalysisRequest) -> GraphState:
    symbol = request.symbol.strip().upper()
    country = _normalize_country(symbol, request.country)
    request_id = str(uuid4())
    logger.info("analysis_request_started", request_id=request_id, symbol=symbol, country=country)
    initial_state = GraphState(
        symbol=symbol,
        country=country,
        horizon=request.horizon.value,
        metadata={"request_id": request_id},
    )
    try:
        result = await graph.ainvoke(initial_state)
    except LLMProviderError as exc:
        logger.exception(
            "analysis_request_failed",
            request_id=request_id,
            symbol=symbol,
            country=country,
            error_type=type(exc).__name__,
        )
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ExternalProviderError as exc:
        logger.exception(
            "analysis_request_failed",
            request_id=request_id,
            symbol=symbol,
            country=country,
            error_type=type(exc).__name__,
        )
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except InvestorOSError as exc:
        logger.exception(
            "analysis_request_failed",
            request_id=request_id,
            symbol=symbol,
            country=country,
            error_type=type(exc).__name__,
        )
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        logger.exception(
            "analysis_request_failed",
            request_id=request_id,
            symbol=symbol,
            country=country,
            error_type=type(exc).__name__,
        )
        raise HTTPException(status_code=500, detail="Analysis failed") from exc

    response = GraphState.model_validate(result)
    response.metadata["request_id"] = request_id
    logger.info("analysis_request_succeeded", request_id=request_id, symbol=symbol, country=country)
    return response


def _normalize_country(symbol: str, country: str | None) -> str:
    if country:
        return country.strip().upper()
    if symbol.endswith((".NS", ".BO")):
        return "IN"
    return "US"
