import os


class Settings:
    INTENT_SERVICE_HOST: str = os.getenv("INTENT_SERVICE_HOST", "localhost")
    INTENT_SERVICE_PORT: int = int(os.getenv("INTENT_SERVICE_PORT", "50051"))

    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    RESPONSE_MODEL_NAME: str = os.getenv("RESPONSE_MODEL_NAME", "gpt-oss:20b")
    OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "120"))

    INTENT_CONFIDENCE_THRESHOLD: float = float(
        os.getenv("INTENT_CONFIDENCE_THRESHOLD", "0.5")
    )

    @property
    def intent_service_target(self) -> str:
        return f"{self.INTENT_SERVICE_HOST}:{self.INTENT_SERVICE_PORT}"


settings = Settings()
