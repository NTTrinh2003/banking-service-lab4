import json

import requests

from app.clients.base import BaseClient


class OllamaClient(BaseClient):
    def generate_json(self, system_prompt: str, user_prompt: str, model: str) -> dict:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
            "format": "json",
        }
        resp = requests.post(url, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        return json.loads(resp.json()["message"]["content"])
