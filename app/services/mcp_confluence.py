from typing import Any, Dict, List

class ConfluenceMCP:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token
    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        # TODO: call Confluence MCP or REST API
        return [{"title": f"Doc about {query}", "url": f"{self.base_url}/display/DOC/{i}", "snippet": "Lorem ipsum …"} for i in range(1, min(limit, 5)+1)]