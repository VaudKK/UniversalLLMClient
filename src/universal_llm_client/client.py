

from collections.abc import AsyncIterator
import time

from universal_llm_client.models.request import LLMRequest
from universal_llm_client.models.responses import LLMResponse
from universal_llm_client.prompts.parameters import GenerationConfig
from universal_llm_client.providers.base import BaseLLMProvider
from universal_llm_client.usage import UsageTracker
from universal_llm_client.observability import logger


class LLMClient:
    def __init__(self,provider: BaseLLMProvider):
        self.provider = provider
        self.usage_tracker = UsageTracker()


    async def generate(
            self,
            prompt: str,
            **kwargs,
    ) -> LLMResponse:
        
        config = GenerationConfig(
            temperature=0.2,
            top_p=1.0,
            max_output_tokens=1000
        )

        request = LLMRequest(
            prompt = prompt,
            generation=config,
            **kwargs,
        )

        start = time.perf_counter()
        
        response = await self.provider.generate(request)

        latency_ms = (
            time.perf_counter() - start
        ) * 1000

        self.usage_tracker.record(
            input_tokens = response.usage.input_tokens,
            output_tokens = response.usage.output_tokens,
        )

        logger.info(
            "llm_request_completed",
            provider = response.provider,
            model = response.model,
            total_tokens = response.usage.total_tokens,
            latency_ms = round(latency_ms, 2)
        )

        return response

    async def stream(
            self,
            prompt: str,
            **kwargs,
    ) -> AsyncIterator[str]:

        request = LLMRequest(
            prompt = prompt,
            **kwargs,
        )

        async for chunk in self.provider.stream(request):
            yield chunk

    async def close(self) -> None:
        await self.provider.close()