from typing import Any, Dict, List, Optional

class VectorDB:
    def __init__(self, url: str):
        self.url = url
    def retrieve(self, query: str, top_k: int = 10, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        # TODO: call your VectorDB (Qdrant/Milvus/Weaviate/pgvector)
        return [
            {"score": 0.83 - i*0.03, "source": f"file_{i}.pdf", "page": i,
             "section": f"H2.{i}", "url": f"https://kb.local/doc/{i}",
             "content": f"Relevant snippet for '{query}' #{i}"}
            for i in range(min(top_k, 5))
        ]