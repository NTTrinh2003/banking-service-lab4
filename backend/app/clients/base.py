from abc import ABC


class BaseClient(ABC):
    def __init__(self, base_url: str = "", timeout: int = 120):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
