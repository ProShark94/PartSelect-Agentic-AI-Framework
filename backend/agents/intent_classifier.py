"""Simple keyword‑based intent classifier.

This agent inspects the user’s message and assigns a coarse intent
category. More sophisticated approaches could leverage machine learning
models or large language models for intent detection; however a simple
keyword search is sufficient for this case study.
"""

from __future__ import annotations

import re
from typing import Any, Dict

from .base_agent import BaseAgent


class IntentClassifier(BaseAgent):
    """Identify the user’s intent from their query."""

    PART_NUMBER_PATTERN = re.compile(r"\b(?:PS\d+|WP[\w\d]+|W\d{5,})\b", re.IGNORECASE)

    def handle(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        q = query.lower()

        # Check for installation/repair/troubleshooting questions
        if any(keyword in q for keyword in ["install", "installation", "fix", "repair", "replace", "broken", "not working", "issue", "problem", "troubleshoot", "how to"]):
            intent = "installation"
        # Check for compatibility questions
        elif any(keyword in q for keyword in ["compatible", "fit", "model", "work with"]):
            intent = "compatibility"
        # Check for order‑related questions
        elif any(keyword in q for keyword in ["order", "return", "refund", "track", "shipping", "delivery"]):
            intent = "order_support"
        # Check for product information (presence of part number or general part query)
        elif self.PART_NUMBER_PATTERN.search(query) or any(keyword in q for keyword in ["part", "parts", "find", "search", "looking for"]):
            intent = "product_info"
        else:
            intent = "general"

        return {"response": intent, "intent": intent}