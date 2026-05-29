import os


class Settings:
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    INTENT_MODEL_NAME: str = os.getenv("INTENT_MODEL_NAME", "gpt-oss:20b")
    GRPC_PORT: int = int(os.getenv("GRPC_PORT", "50051"))
    OLLAMA_TIMEOUT: int = int(os.getenv("OLLAMA_TIMEOUT", "120"))


settings = Settings()
