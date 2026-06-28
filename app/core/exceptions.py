class InvestingAgentError(Exception):
    """Base exception for the application."""


# -----------------------------
# Configuration
# -----------------------------

class ConfigurationError(InvestingAgentError):
    """Raised when configuration is invalid."""


# -----------------------------
# Infrastructure
# -----------------------------

class ExternalServiceError(InvestingAgentError):
    """Base class for external services."""


class MarketDataError(ExternalServiceError):
    """Market provider failed."""


class NewsServiceError(ExternalServiceError):
    """News provider failed."""


class LLMServiceError(ExternalServiceError):
    """LLM provider failed."""


class MemoryServiceError(ExternalServiceError):
    """Vector database failed."""


# -----------------------------
# Business
# -----------------------------

class ValidationError(InvestingAgentError):
    """Invalid user input."""


class AgentExecutionError(InvestingAgentError):
    """Agent execution failed."""


class RecommendationError(InvestingAgentError):
    """Recommendation generation failed."""