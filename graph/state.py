from typing import TypedDict, Optional, Dict, Any

class AgentState(TypedDict):
    stock: str

    market_data: Optional[Dict[str, Any]]
    news_data: Optional[str]
    fundamentals: Optional[Dict[str, Any]]
    technical_data: Optional[Dict[str, Any]]
    forecast: Optional[str]
    risk: Optional[str]
    recommendation: Optional[str]