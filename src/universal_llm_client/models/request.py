from pydantic import BaseModel, Field

class LLMRequest(BaseModel):
    prompt: str = Field(min_length=1)
    model: str | None = None
    system_instruction: str | None = None
    temperature: float | None = Field(
        default = None,
        ge = 0.0,
        le = 2.0,
    )
    max_output_tokens: int = Field(
        default = 1000,
        gt=0,
    )
    metadata: dict[str,str] = Field(
        default_factory = dict,
    )