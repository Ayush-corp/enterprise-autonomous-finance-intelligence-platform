# agents/news_agent.py

from tools.llm_client import call_llm
import requests

def fetch_news(stock):
    # simple hack: you can replace with NewsAPI / scraping
    url = f"https://newsapi.org/v2/everything?q={stock}&apiKey=YOUR_KEY"
    return requests.get(url).json()

def news_agent(state):
    print("News agent processing state:", state)
    articles = fetch_news(state["stock"])

    headlines = [a["title"] for a in articles.get("articles", [])[:10]]

    summary = call_llm(
        system="You are a financial news analyst.",
        user=f"""
        Analyze sentiment and impact of these headlines:
        {headlines}

        Return:
        - sentiment (positive/negative/neutral)
        - key risks
        - catalysts
        """
    )

    state["news_data"] = summary
    return state