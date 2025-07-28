"""Agent for retrieving product information from the local catalogue."""

from __future__ import annotations

import json
import os
import re
from typing import Any, Dict, List, Optional

from .base_agent import BaseAgent


class ProductSearchAgent(BaseAgent):
    """Search for parts in the catalogue and return information.

    In addition to exact lookups by part number or keywords, this agent can
    perform semantic search using an optional vector store. When initialised
    with ``use_vector=True``, it constructs a `VectorStore` over the
    catalogue. Queries that do not directly mention a part number will be
    passed to the vector store to retrieve the most relevant products.
    """

    PART_PATTERN = re.compile(r"\b(PS\d+|WP[\w\d]+|W\d{5,})\b", re.IGNORECASE)

    def __init__(self, data_path: Optional[str] = None, use_vector: bool = False) -> None:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        self.data_file = data_path or os.path.join(base_dir, "data", "products.json")
        self.catalogue: List[Dict[str, Any]] = []
        self._load_catalogue()
        # Initialise vector store if requested
        self.vector_store = None
        if use_vector:
            try:
                from ..vector_store import VectorStore
                self.vector_store = VectorStore(self.data_file)
            except Exception:
                # If vector store initialisation fails, silently continue without it
                self.vector_store = None

    def _load_catalogue(self) -> None:
        if os.path.exists(self.data_file):
            with open(self.data_file, "r", encoding="utf-8") as f:
                self.catalogue = json.load(f)

    def _find_by_part_number(self, part_number: str) -> Optional[Dict[str, Any]]:
        part_number_upper = part_number.upper()
        for item in self.catalogue:
            if item["part_number"].upper() == part_number_upper or part_number_upper in [alt.upper() for alt in item.get("alt_numbers", [])]:
                return item
        return None

    def _search_by_keywords(self, query: str) -> Optional[Dict[str, Any]]:
        q = query.lower()
        for item in self.catalogue:
            if item["name"].lower() in q or any(model.lower() in q for model in item.get("model_compatibility", [])):
                return item
        return None

    def handle(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # Check conversation history for part numbers
        history = context.get("history", [])
        full_conversation = " ".join([msg.get("content", "") for msg in history])
        combined_text = f"{full_conversation} {query}"
        
        # First attempt to identify a part number from current message or history
        match = self.PART_PATTERN.search(combined_text)
        item: Optional[Dict[str, Any]] = None
        if match:
            part_number = match.group(1)
            item = self._find_by_part_number(part_number)
        if not item:
            item = self._search_by_keywords(query)

        if item:
            response = {
                "part_number": item["part_number"],
                "name": item["name"],
                "description": item["description"],
                "model_compatibility": item.get("model_compatibility", []),
                "installation": item.get("installation"),
                "image_url": item.get("image_url"),
            }
            return {"response": response, "agent": "product_search"}

        # Attempt semantic search if a vector store is available and no direct match was found
        if self.vector_store:
            results = self.vector_store.query(query, top_k=1)
            if results:
                similarity, meta = results[0]
                # Only return results with reasonable similarity threshold
                if similarity > 0.1:
                    response = {
                        "part_number": meta["part_number"],
                        "name": meta["name"],
                        "description": meta["description"],
                        "model_compatibility": meta.get("model_compatibility", []),
                        "installation": meta.get("installation"),
                        "image_url": meta.get("image_url"),
                    }
                    return {"response": response, "agent": "product_search", "similarity": similarity}

        # If everything fails, attempt to fetch from PartSelect's live API
        api_item = self._fetch_from_partselect_api(part_number=match.group(1) if match else None)
        if api_item:
            return {"response": api_item, "agent": "product_search", "source": "partselect_api"}
        
        # Enhanced fallback response
        if match:
            part_num = match.group(1)
            return {
                "response": f"I couldn't find part number {part_num} in our current catalog. Please double-check the part number, or provide your appliance's model number so I can help you find the right part.",
                "agent": "product_search"
            }
        else:
            return {
                "response": "Please specify both the part number and the model number of your appliance. You can usually find the model number on a sticker inside the appliance door or on the back panel.",
                "agent": "product_search"
            }

    def _fetch_from_partselect_api(self, part_number: Optional[str]) -> Optional[Dict[str, Any]]:
        """Fetch part details from the PartSelect live API.

        Args:
            part_number: The part number to look up.

        Returns:
            A dictionary with part details or ``None`` if the API is not configured or the call fails.
        """
        import os
        import requests
        if not part_number:
            return None
        api_key = os.getenv("PARTSELECT_API_KEY")
        base_url = os.getenv("PARTSELECT_API_URL", "https://api.partselect.com")
        if not api_key:
            return None
        try:
            url = f"{base_url}/parts/{part_number}"
            headers = {"Authorization": f"Bearer {api_key}"}
            resp = requests.get(url, headers=headers, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                # Map API fields into our internal representation
                return {
                    "part_number": data.get("part_number"),
                    "name": data.get("name"),
                    "description": data.get("description"),
                    "model_compatibility": data.get("models", []),
                    "installation": data.get("installation_instructions"),
                    "image_url": data.get("image_url"),
                }
        except Exception:
            pass
        return None
