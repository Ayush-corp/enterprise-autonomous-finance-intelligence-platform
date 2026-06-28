from typing import TypedDict


class GraphState(TypedDict):

    symbol: str

    market_data: dict

    news_data: dict

    recommendation: dict