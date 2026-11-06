from pydantic_settings import BaseSettings, SettingsConfigDict

class LLMSettings(BaseSettings):
    llm_api_key: str
    llm_api_model: str

    llm_timeout_seconds: float = 30.0
    llm_max_retries: int = 2
    llm_log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file = ".env",
        extra = "ignore",
    )