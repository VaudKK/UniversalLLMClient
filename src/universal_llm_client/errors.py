class LLMError(Exception):
    """Base exception for the library"""


class LLMProviderError(LLMError):
    """Raised when a provider request fails."""


class LLMConfigurationError(LLMError):
    """Raised when provider configuration is invalid"""