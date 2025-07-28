"""Simple vector store for semantic search over the product catalogue.

This module demonstrates how to integrate a vector database into the
PartSelect chat agent without external dependencies such as FAISS or
Weaviate. It uses scikit‑learn's TF‑IDF vectoriser and nearest-neighbour
search to compute similarity between user queries and product documents.

In a production system you might replace this with a dedicated vector
database (e.g., FAISS, Milvus, Pinecone, Weaviate) and use a more
sophisticated embedding model (e.g., OpenAI embeddings). The API is
designed to make swapping the backend straightforward.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors


@dataclass
class Document:
    """Represents a product document to be indexed."""
    text: str
    metadata: Dict[str, Any]


class VectorStore:
    """In‑memory vector store using TF‑IDF and nearest neighbours."""

    def __init__(self, product_file: str) -> None:
        self.product_file = product_file
        self.documents: List[Document] = []
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.nn: NearestNeighbors | None = None
        self._load_products()
        self._build_index()

    def _load_products(self) -> None:
        with open(self.product_file, "r", encoding="utf-8") as f:
            products = json.load(f)
        for p in products:
            text_parts: List[str] = [p.get("name", ""), p.get("description", ""), p.get("instructions", ""), p.get("installation", "")]
            text = "\n".join([t for t in text_parts if t])
            self.documents.append(Document(text=text, metadata=p))

    def _build_index(self) -> None:
        corpus = [doc.text for doc in self.documents]
        self.matrix = self.vectorizer.fit_transform(corpus)
        self.nn = NearestNeighbors(n_neighbors=min(5, len(self.documents)), metric="cosine")
        self.nn.fit(self.matrix)

    def query(self, text: str, top_k: int = 3) -> List[Tuple[float, Dict[str, Any]]]:
        """Return the top_k most similar documents to the query text.

        Args:
            text: The user query.
            top_k: Number of results to return.

        Returns:
            A list of tuples of (similarity score, product metadata).
        """
        if self.nn is None:
            return []
        query_vec = self.vectorizer.transform([text])
        distances, indices = self.nn.kneighbors(query_vec, n_neighbors=top_k)
        results: List[Tuple[float, Dict[str, Any]]] = []
        for dist, idx in zip(distances[0], indices[0]):
            # convert cosine distance to similarity (1 - distance)
            similarity = 1.0 - dist
            meta = self.documents[idx].metadata
            results.append((similarity, meta))
        return results