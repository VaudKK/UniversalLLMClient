import pytest

from universal_llm_client.client import LLMClient
from universal_llm_client.client import LLMClient
from universal_llm_client.config import LLMSettings
from universal_llm_client.providers.openai import OpenAIProvider



@pytest.fixture
def settings():
    return LLMSettings(
        llm_api_key = "test_api_key",
        llm_api_model = "test-model",
        llm_timeout_seconds = 10,
        llm_max_retries = 2,
    )


@pytest.fixture
def llm_client(settings):
    provider = OpenAIProvider(settings)
    return LLMClient(provider)