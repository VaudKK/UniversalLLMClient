

from openai import AsyncOpenAI
import openai
import openai

from universal_llm_client.config import LLMSettings
from universal_llm_client.errors import LLMProviderError
from universal_llm_client.models.request import LLMRequest
from universal_llm_client.models.responses import LLMResponse, TokenUsage
from universal_llm_client.providers.base import BaseLLMProvider
from universal_llm_client.retry import with_retry


class OpenAIProvider(BaseLLMProvider):

    def __init__(self, settings: LLMSettings):
        self.settings = settings

        self.client = AsyncOpenAI(
            api_key = settings.openai_api_key,
            timeout = settings.llm_timeout_seconds,

            max_retries = 0,
        )


    @with_retry
    async def generate(
            self,
            request: LLMRequest,
    ) -> LLMResponse:

        model = request.model or self.settings.openai_model

        try:
            params = {
                "model": model,
                "input": request.prompt,
                "max_output_tokens": request.max_output_tokens,
            }

            if request.system_instruction:
                params["instructions"] = request.system_instruction


            if request.temperature is not None:
                params["temperature"] = request.temperature


            result = await self.client.responses.create(**params)

            usage = result.usage

            return LLMResponse(
                content = result.output_text,
                model = model,
                provider = "openai",
                usage = TokenUsage(
                    input_tokens = usage.input_tokens if usage else 0,
                    output_tokens = usage.output_tokens if usage else 0,
                    total_tokens = usage.total_tokens if usage else 0,
                ),
                request_id = result.id,
            )
    
        except openai.APIError as exc:
            raise LLMProviderError(
                f"OpenAI request failed: {type(exc).__name__}"
            ) from exc



    async def close(self) -> None:
        await self.client.close()