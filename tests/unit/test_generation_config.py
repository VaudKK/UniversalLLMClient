
import pytest
from pydantic import ValidationError

from universal_llm_client.prompts.parameters import GenerationConfig


def test_default_generation_config():
    config = GenerationConfig()

    assert config.temperature == 0.2
    assert config.top_p == 1.0
    assert config.max_output_tokens == 1000


def test_valid_generation_config():
    config = GenerationConfig(
        temperature=0.7,
        top_p=0.5,
        max_output_tokens=500
    )

    assert config.temperature == 0.7
    assert config.top_p == 0.5
    assert config.max_output_tokens == 500


def test_invalid_temperature():
    with pytest.raises(ValidationError):
        GenerationConfig(temperature=2.5)


def test_invalid_top_p():
    with pytest.raises(ValidationError):
        GenerationConfig(top_p=0)


def test_invalid_max_output_tokens():
    with pytest.raises(ValidationError):
        GenerationConfig(max_output_tokens=0)
