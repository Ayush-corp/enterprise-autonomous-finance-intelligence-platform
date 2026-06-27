def risk_agent(state):
    print("Risk agent processing state:", state)
    state["risk"] = {
        "risk_level": "medium"
    }

    return state