from litellm import completion

class LocalLLM:
    def __init__(self, backend="ollama", model="llama3.1:8b", temperature=0.2, top_p=0.9, max_tokens=1024):
        self.backend = backend
        self.model = model
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens

    def _to_model(self):
        return f"ollama/{self.model}"

    def complete(self, prompt: str) -> str:
        resp = completion(
            model=self._to_model(),
            messages=[
                {"role": "system", "content": "You are a precise system design expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.temperature,
            top_p=self.top_p,
            max_tokens=self.max_tokens,
        )
        return resp.choices[0].message["content"]
