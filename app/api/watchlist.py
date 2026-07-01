from fastapi import APIRouter
from pydantic import BaseModel, Field

from domain.prediction import WatchlistSymbol
from services.watchlist_service import WatchlistService


router = APIRouter(prefix="/api/v1/watchlist", tags=["Watchlist"])


class WatchlistRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=32)
    country: str | None = Field(default=None, min_length=2, max_length=2)


@router.post("", response_model=WatchlistSymbol)
def add_symbol(request: WatchlistRequest) -> WatchlistSymbol:
    return WatchlistService().add_symbol(request.symbol, request.country)


@router.get("", response_model=list[WatchlistSymbol])
def list_watchlist() -> list[WatchlistSymbol]:
    return WatchlistService().seed_default_watchlist()


@router.delete("/{symbol}")
def remove_symbol(symbol: str) -> dict[str, str]:
    WatchlistService().remove_symbol(symbol)
    return {"status": "removed", "symbol": symbol.upper()}
