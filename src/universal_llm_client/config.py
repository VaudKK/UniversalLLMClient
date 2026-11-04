from pydantic_settings import BaseSettings, SettingsConfigDict

class LLMSettings(BaseSettings):
    openai_api_key: str
    openai_model: str

    llm_timeout_seconds: float = 30.0
    llm_max_retries: int = 2
    llm_log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file = ".env",
        extra = "ignore",
    )