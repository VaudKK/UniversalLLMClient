# Universal LLM Client

A reusable, provider-agnostic Python library for integrating Large Language Models (LLMs) into applications through a consistent interface.

## Overview

Universal LLM Client provides a unified interface for interacting with different LLM providers without coupling application code to provider-specific SDKs or API implementations.

The library uses a provider adapter architecture to normalize requests and responses, making it easier to integrate, test, and extend LLM-powered applications.

The initial implementation supports OpenAI, with an architecture designed to accommodate additional providers in the future.

## Key Features

- **Provider abstraction:** Interact with LLMs through a common interface.
- **Normalized responses:** Convert provider-specific responses into a consistent response model.
- **Asynchronous execution:** Support asynchronous LLM requests.
- **Streaming support:** Receive generated text incrementally.
- **Configuration management:** Manage API credentials and model settings through environment variables.
- **Error handling:** Normalize provider errors for consistent application handling.
- **Retry mechanism:** Retry eligible transient failures using bounded exponential backoff.
- **Usage tracking:** Track input tokens, output tokens, and total token consumption.
- **Structured logging:** Capture request metadata, latency, and execution status.
- **Automated testing:** Test core functionality and provider integrations using mocked HTTP responses.

## Architecture

The library follows a provider adapter architecture.

Application code communicates with `LLMClient`, which delegates requests to the configured provider implementation.

Each provider adapter handles provider-specific API communication and converts responses into the common response model.

```text
Application
    |
    v
LLMClient
    |
    v
BaseLLMProvider
    |
    +-------------------+
    |                   |
    v                   v
OpenAIProvider     FutureProvider
    |
    v
OpenAI API
```

### Main Components

| Component | Responsibility |
|---|---|
| LLMClient | Public interface used by applications |
| BaseLLMProvider | Defines the provider contract |
| OpenAIProvider | Handles OpenAI API integration |
| LLMRequest | Validates and represents LLM requests |
| LLMResponse | Standardizes LLM responses |
| TokenUsage | Represents token consumption |
| UsageTracker | Aggregates usage statistics |
| Retry module | Handles eligible transient failures |
| Observability module | Supports structured logging and monitoring |

## Technology Stack

- Python 3.12+
- OpenAI Python SDK
- Pydantic v2
- Pydantic Settings
- HTTPX
- Tenacity
- structlog
- pytest
- pytest-asyncio
- respx
- uv

## Project Structure

```text
universal-llm-client/
│
├── pyproject.toml
├── .env.example
├── README.md
│
├── src/
│   └── universal_llm_client/
│       ├── __init__.py
│       ├── client.py
│       ├── config.py
│       ├── errors.py
│       ├── retry.py
│       ├── observability.py
│       │
│       ├── models/
│       │   ├── __init__.py
│       │   ├── request.py
│       │   └── responses.py
│       │
│       └── providers/
│           ├── __init__.py
│           ├── base.py
│           └── openai.py
│
├── tests/
│   ├── unit/
│   └── integration/
│
└── examples/
    ├── basic_completion.py
    └── streaming.py
```

*Adjust this tree to match the actual files in your repository.*

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd universal-llm-client
```

Install dependencies using uv:

```bash
uv sync
```

## Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your-api-key
OPENAI_MODEL=your-supported-model
LLM_TIMEOUT_SECONDS=30
LLM_MAX_RETRIES=2
LLM_LOG_LEVEL=INFO
```

Do not commit your `.env` file or expose API credentials.

Use `.env.example` to document the required environment variables without including real secrets.

## Basic Usage

Example of using the client:

```python
from universal_llm_client.client import LLMClient
from universal_llm_client.providers.openai import OpenAIProvider
from universal_llm_client.config import LLMSettings

settings = LLMSettings()

provider = OpenAIProvider(settings)
llm = LLMClient(provider)

async def main():
    try:
        response = await llm.generate(
            prompt="Explain dependency injection in simple terms.",
            temperature=0.7,
            max_output_tokens=500,
        )

        print(response.content)
        print(response.usage)

    finally:
        await llm.close()
```

*This example assumes your current `LLMClient.generate()` method accepts these arguments. Update it if your public interface differs.*

## Streaming Usage

The library also supports incremental text generation.

```python
async def stream_example():
    request = LLMRequest(
        prompt="Explain how asynchronous programming works."
    )

    async for chunk in provider.stream(request):
        print(chunk, end="", flush=True)
```

## Error Handling

The library provides a consistent error-handling approach across provider integrations.

Examples of failures include:

- Authentication errors
- Invalid requests
- Rate-limit errors
- API timeouts
- Network connectivity failures
- Provider service errors

Transient failures may be retried according to the configured retry policy. Permanent errors should be surfaced without unnecessary retries.

## Usage Tracking

The library tracks token consumption for successful requests.

Example:

```python
print(llm.usage_tracker.input_tokens)
print(llm.usage_tracker.output_tokens)
print(llm.usage_tracker.total_tokens)
print(llm.usage_tracker.request_count)
```

Update these examples to match the actual public API.

## Testing

Run the complete test suite:

```bash
uv run pytest -v
```

Run unit tests:

```bash
uv run pytest tests/unit -v
```

Run integration tests:

```bash
uv run pytest tests/integration -v
```

Integration tests use mocked HTTP responses to verify provider behavior without requiring live API calls.

## Current Limitations

- OpenAI is the initial supported provider.
- Model capabilities vary by provider and model.
- Token usage depends on the usage information returned by the provider.
- Retry behavior is limited to configured transient errors.
- Streaming and structured-output capabilities may differ between providers.

## Future Improvements

- Add Anthropic and Google provider adapters.
- Introduce model capability discovery.
- Add structured output support.
- Add tool/function calling support.
- Improve provider-independent error classification.
- Add request-level tracing and cost estimation.
- Add comprehensive streaming integration tests.

## Development Roadmap

This project is part of a broader AI Engineering learning roadmap.

The immediate objective is to establish a reliable LLM integration foundation before progressing into:

1. Advanced Retrieval-Augmented Generation (RAG).
2. Autonomous AI agents and tool orchestration.
3. Production AI systems and enterprise architecture.

## Contributing

Contributions and suggestions are welcome.

When contributing:

1. Create a feature branch.
2. Add or update relevant tests.
3. Run the test suite.
4. Update documentation where necessary.
5. Submit a pull request describing the changes.

## License

Add your chosen open-source license here before publishing the repository.
