"""Intent classifier based on large language models.

This agent uses either the OpenAI API or the Deepseek API to classify user
queries into one of several predefined intents. It sends a prompt to the
language model asking it to respond with a single word indicating the
intent. Fallback to the keyword classifier if LLM calls fail.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

from .base_agent import BaseAgent
from .openai_agent import OpenAIAgent
from .deepseek_agent import DeepSeekAgent
from .intent_classifier import IntentClassifier  # for fallback


class LLMIntentClassifier(BaseAgent):
    """Use a language model to determine the user’s intent."""

    INTENTS = ["product_info", "compatibility", "installation", "order_support", "general"]

    def __init__(self, openai_agent: Optional[OpenAIAgent] = None, deepseek_agent: Optional[DeepSeekAgent] = None) -> None:
        self.openai_agent = openai_agent or OpenAIAgent()
        self.deepseek_agent = deepseek_agent or DeepSeekAgent()
        self.fallback_classifier = IntentClassifier()

    def handle(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        prompt = (
            "You are an intent classification engine for an e‑commerce appliance parts chatbot. "
            "Given a user query, respond with one of the following intent labels: "
            f"{', '.join(self.INTENTS)}. "
            "Return only the label without any explanation. "
            f"Query: {query}"
        )
        # Try OpenAI first
        answer = self.openai_agent.call(prompt)
        if answer is None:
            answer = self.deepseek_agent.call(prompt)
        if answer:
            intent = answer.strip().split()[0].lower()
            if intent not in self.INTENTS:
                # Unexpected response; fallback
                fallback = self.fallback_classifier.handle(query, context)
                intent = fallback.get("intent")
            return {"response": intent, "intent": intent, "source": "llm"}
        # Fallback to keyword classifier
        return self.fallback_classifier.handle(query, context)