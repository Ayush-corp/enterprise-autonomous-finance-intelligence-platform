# agents/committee_agent.py

from tools.llm_client import call_llm

def committee_agent(state):
    print("Committee agent processing state:", state)
    decision = call_llm(
        system="You are head of an investment committee managing risk-adjusted returns.",
        user=f"""
        MARKET:
        {state['market_data']}

        NEWS:
        {state['news_data']}

        TECHNICAL:
        {state['technical_data']}

        FORECAST:
        {state['forecast']}

        FUNDAMENTALS:
        {state['fundamentals']}

        TASK:
        Decide final action: BUY / SELL / HOLD

        Return:
        - decision
        - reasoning
        - risk score (0-100)
        - position size suggestion (% capital)
        """
    )

    state["recommendation"] = decision

    # save memory
    state["memory"] = decision

    return state