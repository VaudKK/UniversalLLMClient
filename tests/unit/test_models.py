from pydantic import ValidationError
import pytest

from universal_llm_client.models.request import LLMRequest


def test_valid_request():
    request = LLMRequest(
        prompt="Hello, world!",
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_output_tokens=100,
    )

    assert request.prompt == "Hello, world!"
    assert request.model == "gpt-3.5-turbo"
    assert request.temperature == 0.7
    assert request.max_output_tokens == 100



def test_empty_prompt_is_rejected():
    with pytest.raises(ValidationError):
        LLMRequest(prompt="")


def test_negative_temperature_is_rejected():
    with pytest.raises(ValidationError):
        LLMRequest(prompt="Hello", model="gpt-3.5-turbo", temperature=-0.1)