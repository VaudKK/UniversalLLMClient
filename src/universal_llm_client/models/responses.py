from pydantic import BaseModel,Field
from typing import Literal

class TokenUsage(BaseModel):
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0


class LLMResponse(BaseModel):
    content: str
    model: str
    provider: str
    usage: TokenUsage
    request_id: str | None = None
    finish_reason: str | None = None


class CodeReviewFinding(BaseModel):
    category: Literal["bug","security","performance"]
    severity: Literal["LOW","MEDIUM","HIGH","CRITICAL"]
    description: str = Field(min_length=1)
    suggested_fix: str = Field(min_length=1)

class CodeReviewResponse(BaseModel):
    findings: list[CodeReviewFinding] = Field(default_factory=list)
