def decision_agent(state):
    print("Decision agent processing state:", state)
    market = state["market_data"]
    forecast = state["forecast"]

    close = market["close"]
    sma = market["sma20"]

    if close > sma:
        decision = "BUY"
    elif close < sma:
        decision = "SELL"
    else:
        decision = "HOLD"

    state["recommendation"] = {
        "decision": decision,
        "forecast": forecast,
        "risk": state["risk"]
    }

    return state