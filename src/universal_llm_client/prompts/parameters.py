from pydantic import BaseModel,Field

class GenerationConfig(BaseModel):
    temperature: float = Field(ge=0.0,le=2.0,default=0.2)
    top_p: float = Field(gt=0,le=1.0,default=1.0)
    max_output_tokens: int = Field(gt=0,default=1000)