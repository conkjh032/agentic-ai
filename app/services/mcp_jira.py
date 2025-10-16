from typing import Any, Dict, List

class JiraMCP:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url
        self.token = token
    def search(self, jql: str, limit: int = 10) -> List[Dict[str, Any]]:
        # TODO: call Jira MCP or Jira REST API
        return [{"key": f"JIRA-{i}", "summary": f"Dummy issue for {jql}", "url": f"{self.base_url}/browse/JIRA-{i}"} for i in range(1, min(limit, 5)+1)]