"""Agent for handling order support queries."""

from __future__ import annotations

from typing import Any, Dict

from .base_agent import BaseAgent


class OrderSupportAgent(BaseAgent):
    """Provide generic responses for order‑related questions."""

    def handle(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # In a real system this agent would integrate with order management APIs.
        # Here we provide simple canned responses based on keywords.
        q = query.lower()
        if "status" in q or "track" in q:
            response = (
                "You can track your order by logging into your PartSelect account "
                "and navigating to the 'My Orders' section. If you need further assistance, "
                "please provide your order number."
            )
        elif "return" in q or "refund" in q:
            response = (
                "To initiate a return or refund, please visit our returns page or contact customer service at 1‑800‑123‑4567."
            )
        elif "cancel" in q:
            response = (
                "Orders may be cancelled before they are shipped. Please call our support line immediately to request a cancellation."
            )
        else:
            response = (
                "For questions about ordering, shipping or returns, please visit the support centre on PartSelect.com or call us for assistance."
            )
        return {"response": response, "agent": "order_support"}