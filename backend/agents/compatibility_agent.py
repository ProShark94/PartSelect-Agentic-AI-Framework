"""Agent for verifying part compatibility with an appliance model."""

from __future__ import annotations

import re
from typing import Any, Dict, Optional

from .base_agent import BaseAgent
from .product_search_agent import ProductSearchAgent


class CompatibilityAgent(BaseAgent):
    """Check whether a given part works with a specific appliance model."""

    # Match tokens that contain at least one digit (typical for model numbers)
    MODEL_PATTERN = re.compile(r"\b[A-Z]*\d+[A-Z0-9]*\b", re.IGNORECASE)

    def __init__(self, product_agent: Optional[ProductSearchAgent] = None) -> None:
        self.product_agent = product_agent or ProductSearchAgent()

    def handle(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Respond to a compatibility query.

        Attempts to extract both a part number and an appliance model from the
        user's message. The part number is identified using the product
        agent's pattern; the model is assumed to be another alphanumeric token
        (≥5 characters) that is not the part number itself.
        """
        # Check conversation history for part numbers and models
        history = context.get("history", [])
        full_conversation = " ".join([msg.get("content", "") for msg in history])
        combined_text = f"{full_conversation} {query}"
        
        # Find all uppercase alphanumeric tokens of length >=5
        tokens = [t for t in self.MODEL_PATTERN.findall(combined_text)]
        part_match = self.product_agent.PART_PATTERN.search(combined_text)
        part_number: Optional[str] = None
        model: Optional[str] = None
        
        if part_match:
            part_number = part_match.group(1)
            # Remove the part number from tokens (case insensitive)
            tokens_filtered = [t for t in tokens if t.lower() != part_number.lower()]
        else:
            tokens_filtered = tokens
            
        # Take the first remaining token as model if available
        if tokens_filtered:
            model = tokens_filtered[0]

        if not part_number and not model:
            return {"response": "Please specify both the part number and the model number.", "agent": "compatibility"}
        elif not part_number:
            return {"response": f"I can see model {model}, but I need the part number too. What part are you asking about?", "agent": "compatibility"}
        elif not model:
            return {"response": f"I can see part number {part_number}, but I need your appliance model number to check compatibility.", "agent": "compatibility"}

        item = self.product_agent._find_by_part_number(part_number)
        if item:
            compatibility_list = [m.upper() for m in item.get("model_compatibility", [])]
            if model.upper() in compatibility_list:
                return {"response": f"Yes, part {part_number} is compatible with model {model.upper()}.", "agent": "compatibility"}
            return {"response": f"No, part {part_number} is not listed as compatible with model {model.upper()}.", "agent": "compatibility"}
        return {"response": f"I couldn't find part {part_number} in our catalogue.", "agent": "compatibility"}