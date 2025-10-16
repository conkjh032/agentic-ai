from typing import List, Dict

class LLMClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
    def call(self, *, model: str, messages: List[Dict[str, str]], temperature: float = 0.2, max_tokens: int = 1024) -> str:
        # TODO: replace with real HTTP call to your company LLM
        prompt = "\n".join(f"[{m['role']}] {m['content']}" for m in messages)
        return f"[model={model}] Simulated answer based on: {prompt[:240]} …"