from typing import Any, Dict
import time

class PrometheusMCP:
    def __init__(self, base_url: str):
        self.base_url = base_url
    def query_range(self, promql: str, start: int, end: int, step: int) -> Dict[str, Any]:
        # TODO: call Prometheus MCP /api/v1/query_range
        return {"promql": promql, "stats": {"avg": 123.4, "p95": 456.7, "max": 789.0}, "series_count": 3}