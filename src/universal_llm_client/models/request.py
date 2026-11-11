from pydantic import BaseModel, Field
from universal_llm_client.prompts.parameters import GenerationConfig

class LLMRequest(BaseModel):
    prompt: str = Field(min_length=1)
    model: str | None = None
    system_instruction: str | None = None
    generation: GenerationConfig
    metadata: dict[str,str] = Field(
        default_factory = dict,
    )