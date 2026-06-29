class InvestorOSError(Exception):
    """Base exception for InvestorOS."""


class InvestingAgentError(InvestorOSError):
    """Backward-compatible base exception name."""


# -----------------------------
# Configuration
# -----------------------------

class ConfigurationError(InvestingAgentError):
    """Raised when configuration is invalid."""


# -----------------------------
# Infrastructure
# -----------------------------

class ExternalProviderError(InvestorOSError):
    """External provider failed."""


class ExternalServiceError(ExternalProviderError):
    """Base class for external services."""


class MarketDataError(ExternalServiceError):
    """Market provider failed."""


class NewsServiceError(ExternalServiceError):
    """News provider failed."""


class LLMProviderError(ExternalProviderError):
    """LLM provider failed."""


class LLMServiceError(LLMProviderError):
    """Backward-compatible LLM error name."""


class MemoryServiceError(ExternalServiceError):
    """Vector database failed."""


# -----------------------------
# Business
# -----------------------------

class ValidationError(InvestorOSError):
    """Invalid user input."""


class AgentExecutionError(InvestorOSError):
    """Agent execution failed."""


class InvalidGraphStateError(InvestorOSError):
    """Graph state is missing required upstream data."""


class DataUnavailableError(InvestorOSError):
    """Required data was unavailable."""


class RecommendationError(InvestorOSError):
    """Recommendation generation failed."""
