import json
import urllib.request
import os

class GitHubModelsRAG:
    def __init__(self) -> None:
        self.endpoint = "https://models.inference.ai.azure.com"
        self.token = os.environ.get("GitHubModels")
        self.model_name = "gpt-4o-mini"

    def process(self, query: str, context: list) -> str:
        if not self.token:
            return "Error: GITHUB_TOKEN environment variable is missing for RAG module."

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        # Build prompt from context
        context_str = "\n".join([str(c) for c in context])
        
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Use the following documents to answer the user's query."
                },
                {
                    "role": "user",
                    "content": f"Context:\n{context_str}\n\nQuery: {query}"
                }
            ]
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(f"{self.endpoint}/chat/completions", data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error connecting to GitHub Models API: {e}"
