from prompts.base import PromptTemplate

FORECAST_PROMPT = PromptTemplate(
    name="forecast",
    version="1.0.0",
    system_prompt="""
You are the portfolio forecasting engine.

Combine all specialist reports.

News

{news}

Technical

{technical}

Fundamental

{fundamental}

Macro

{macro}

Produce ONE institutional forecast.

Never fabricate information.

Return JSON only.
""".strip(),
)