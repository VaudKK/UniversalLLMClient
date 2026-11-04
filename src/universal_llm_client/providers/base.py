from abc import ABC, abstractmethod

from universal_llm_client.models.request import LLMRequest
from universal_llm_client.models.responses import LLMResponse


class BaseLLMProvider(ABC):

    @abstractmethod
    async def generate(
            self,
            request: LLMRequest,
    ) -> LLMResponse:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass