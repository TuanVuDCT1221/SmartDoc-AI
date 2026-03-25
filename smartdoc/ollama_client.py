from __future__ import annotations

import json
from urllib import error, request


class OllamaClient:
    def __init__(
        self,
        base_url: str,
        model: str,
        timeout_seconds: int = 600,
        temperature: float = 0.1,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds
        self.temperature = temperature

    def health_check(self) -> tuple[bool, str]:
        try:
            with request.urlopen(f"{self.base_url}/api/tags", timeout=5) as response:
                payload = json.loads(response.read().decode("utf-8"))
            models = payload.get("models", [])
            available = {item.get("name", "") for item in models}
            if self.model in available:
                return True, f"Ollama is reachable and model `{self.model}` is available."
            return False, f"Ollama is reachable but model `{self.model}` is missing."
        except Exception as exc:  # noqa: BLE001
            return False, f"Cannot reach Ollama at {self.base_url}: {exc}"

    def generate(self, prompt: str) -> str:
        body = json.dumps(
            {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                },
            }
        ).encode("utf-8")
        req = request.Request(
            url=f"{self.base_url}/api/generate",
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"Ollama HTTP error {exc.code}: {detail}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"Cannot connect to Ollama: {exc.reason}") from exc

        answer = payload.get("response", "").strip()
        if not answer:
            raise RuntimeError("Ollama returned an empty response.")
        return answer
