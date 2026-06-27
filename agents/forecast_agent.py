# agents/forecast_agent.py

from tools.llm_client import call_llm

def forecast_agent(state):
    print("Forecast agent processing state:", state)
    tech = state["technical_data"]

    prediction = call_llm(
        system="You are a quantitative analyst.",
        user=f"""
        Given:
        Close: {tech['close']}
        RSI: {tech['rsi']}
        SMA20: {tech['sma20']}
        Volatility: {tech['volatility']}

        Predict:
        - next 5 day trend (up/down/sideways)
        - confidence (0-1)
        - target price range
        """
    )

    state["forecast"] = prediction
    return state