from universal_llm_client.config import LLMSettings
from universal_llm_client.errors import LLMProviderError
from universal_llm_client.providers.base import BaseLLMProvider
from universal_llm_client.models.request import LLMRequest
from universal_llm_client.models.responses import LLMResponse, TokenUsage

from collections.abc import AsyncIterator

from anthropic import AsyncAnthropic

import anthropic

import httpx


class AnthropicProvider(BaseLLMProvider):

    def __init__(
            self,
            settings: LLMSettings
            ):
        self.settings = settings
        self.http_client = httpx.AsyncClient()
        self.client = AsyncAnthropic(
            max_retries=settings.llm_max_retries,
            api_key=settings.llm_api_key,
        )


    async def generate(self, request: LLMRequest) -> LLMResponse:

        model = request.model or self.settings.llm_api_model

        try:
            result = await self.client.messages.create(
                max_tokens=request.generation.max_output_tokens,
                messages=[
                    {
                        "role": "user",
                        "content": request.prompt
                    }
                ],
                model = model
            )

            return LLMResponse(
                model=model,
                content=result.content[0].text,
                provider="anthropic",
                usage=TokenUsage(
                                    input_tokens=result.usage.input_tokens if result.usage else 0,
                                    output_tokens=result.usage.output_tokens if result.usage else 0,
                                    total_tokens= result.usage.input_tokens + result.usage.output_tokens,
                                ),
                finish_reason=result.stop_reason,
            )
        except anthropic.APIStatusError as exc:
            raise LLMProviderError(
                    f"Anthropic request failed: {type(exc).__name__}"
                ) from exc


    async def stream(self, request: LLMRequest) -> AsyncIterator[str]:

        model = request.model or self.settings.llm_api_model

        try:
            async with self.client.messages.stream(
                max_tokens=request.generation.max_output_tokens,
                messages=[
                    {
                        "role":"user",
                        "content": request.prompt,
                    }
                ],
                model=model,
            ) as stream:
                async for text in stream.text_stream:
                    yield text

        except anthropic.APIStatusError as exc:
            raise LLMProviderError(
                    f"Anthropic request failed: {type(exc).__name__}"
                ) from exc



    async def close(self) ->  None:
        await self.client.close()