from __future__ import annotations

import json
from pathlib import Path

from app.models.domain import RetrievedDocument


class RetrievalService:
    """
    Simple keyword-overlap retriever for demo purposes.

    In a production build, replace this with a proper hybrid/vector retrieval stack.
    """

    def __init__(self, data_path: str = "app/data/sample_documents.json") -> None:
        self.data_path = Path(data_path)
        self._documents = self._load_documents()

    def _load_documents(self) -> list[dict]:
        if not self.data_path.exists():
            return []
        return json.loads(self.data_path.read_text(encoding="utf-8"))

    def ingest(self, doc_id: str, title: str, classification: str, content: str) -> None:
        self._documents.append(
            {
                "doc_id": doc_id,
                "title": title,
                "classification": classification,
                "content": content,
            }
        )
        self.data_path.write_text(json.dumps(self._documents, indent=2), encoding="utf-8")

    def search(self, query: str, scope: list[str], top_k: int = 5) -> list[RetrievedDocument]:
        terms = set(t.strip(".,!?").lower() for t in query.split() if t.strip())
        matches: list[RetrievedDocument] = []

        for doc in self._documents:
            if doc["classification"] not in scope:
                continue

            haystack = f'{doc["title"]} {doc["content"]}'.lower()
            overlap = sum(1 for term in terms if term in haystack)
            if overlap == 0:
                continue

            score = round(min(0.99, overlap / max(len(terms), 1) + 0.15), 2)
            matches.append(
                RetrievedDocument(
                    doc_id=doc["doc_id"],
                    title=doc["title"],
                    classification=doc["classification"],
                    content=doc["content"],
                    score=score,
                )
            )

        matches.sort(key=lambda d: d.score, reverse=True)
        return matches[:top_k]
