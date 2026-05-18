from .GitHubModelsRAG import GitHubModelsRAG

_instance = GitHubModelsRAG()

def process(query: str, context: list) -> str:
    return _instance.process(query, context)
