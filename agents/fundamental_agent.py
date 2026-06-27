def fundamental_agent(state):
    print("Fundamental agent processing state:", state)
    state["fundamentals"] = {
        "score": 7,
        "valuation": "fair",
        "growth": "stable"
    }
    return state