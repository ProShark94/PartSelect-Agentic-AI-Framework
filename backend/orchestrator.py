"""
Multi-Agent Message Orchestrator.

This module coordinates the routing of user messages to specialized agents
based on intent classification, providing a unified interface for the
PartSelect customer service system.

The orchestrator manages multiple AI models and fallback systems to ensure
reliable responses across various query types including product search,
installation guidance, compatibility checks, and general support.
"""

from __future__ import annotations

from typing import Any, Dict, List

from agents.intent_classifier import IntentClassifier
from agents.product_search_agent import ProductSearchAgent
from agents.compatibility_agent import CompatibilityAgent
from agents.installation_agent import InstallationAgent
from agents.order_support_agent import OrderSupportAgent
from agents.openai_agent import OpenAIAgent
from agents.deepseek_agent import DeepSeekAgent
from agents.working_huggingface_agent import WorkingHuggingFaceAgent
from agents.smart_fallback import SmartFallbackSystem


class Orchestrator:
    """
    Coordinates multiple specialized agents to provide comprehensive customer support.
    
    This class manages the entire conversation flow, from intent classification
    to agent selection and response generation, with intelligent fallback
    mechanisms to ensure reliable service availability.
    """

    def __init__(self) -> None:
        """
        Initialize the orchestrator with all available agents and models.
        
        Sets up the agent ecosystem including product search, compatibility checking,
        installation guidance, and multiple AI models for general queries.
        """
        self.product_agent = ProductSearchAgent(use_vector=True)
        self.compatibility_agent = CompatibilityAgent(self.product_agent)
        self.openai_agent = OpenAIAgent()
        self.deepseek_agent = DeepSeekAgent()
        
        try:
            self.huggingface_agent = WorkingHuggingFaceAgent()
        except Exception:
            self.huggingface_agent = None
            
        self.smart_fallback = SmartFallbackSystem()
        
        try:
            from agents.llm_intent_classifier import LLMIntentClassifier
            if self.openai_agent.api_key or self.deepseek_agent.api_key:
                self.intent_classifier = LLMIntentClassifier(
                    openai_agent=self.openai_agent,
                    deepseek_agent=self.deepseek_agent,
                )
            else:
                self.intent_classifier = IntentClassifier()
        except Exception:
            self.intent_classifier = IntentClassifier()
            
        self.installation_agent = InstallationAgent(
            product_agent=self.product_agent,
            openai_agent=self.openai_agent,
            deepseek_agent=self.deepseek_agent,
        )
        self.order_support_agent = OrderSupportAgent()

    def handle_message(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a user message and route it to the appropriate agent.
        
        This method performs intent classification, selects the most suitable
        agent based on the user's query, and manages conversation context
        to maintain continuity across the chat session.
        
        Parameters
        ----------
        message : str
            The user's input message to be processed.
        context : Dict[str, Any]
            Conversation context dictionary containing message history,
            identified parts, and session state. Modified in-place.
        
        Returns
        -------
        Dict[str, Any]
            Response dictionary containing:
            - response: The agent's generated response text
            - agent: Identifier of the agent that handled the request
            - intent: Classified intent category
        """
        history: List[Dict[str, str]] = context.setdefault("history", [])
        history.append({"role": "user", "content": message})

        intent_result = self.intent_classifier.handle(message, context)
        intent = intent_result.get("intent")

        if intent == "product_info":
            result = self.product_agent.handle(message, context)
        elif intent == "compatibility":
            result = self.compatibility_agent.handle(message, context)
        elif intent == "installation" and any(word in message.lower() for word in ['install', 'replace part', 'how to install', 'installation guide']):
            result = self.installation_agent.handle(message, context)
        elif intent == "order_support" and any(word in message.lower() for word in ['order', 'delivery', 'shipping', 'tracking']):
            result = self.order_support_agent.handle(message, context)
        else:
            result = self._handle_general_query(message)

        history.append({"role": "assistant", "content": str(result.get("response"))})
        return result
    
    def _handle_general_query(self, message: str) -> Dict[str, Any]:
        """
        Handle general queries using available AI models with fallback hierarchy.
        
        Attempts to use AI models in priority order: OpenAI -> DeepSeek ->
        Smart Fallback -> HuggingFace, ensuring at least one response is provided.
        
        Parameters
        ----------
        message : str
            The user's query message.
        
        Returns
        -------
        Dict[str, Any]
            Response dictionary with generated answer and model identifier.
        """
        prompt = (
            "You are an assistant for an e‑commerce appliance parts site. "
            "Answer the following question in a concise, friendly manner: "
            f"{message}"
        )
        
        answer = self.openai_agent.call(prompt)
        if answer and answer.strip() and "error" not in answer.lower():
            return {"response": answer, "agent": "general_openai"}
            
        answer = self.deepseek_agent.call(prompt)
        if answer and answer.strip() and "error" not in answer.lower():
            return {"response": answer, "agent": "general_deepseek"}
            
        answer = self.smart_fallback.get_smart_response(message)
        if answer and answer.strip() and len(answer) > 20:
            return {"response": answer, "agent": "general_smart_fallback"}
            
        if self.huggingface_agent and self.huggingface_agent.is_available():
            answer = self.huggingface_agent.call(message)
            if answer and answer.strip() and len(answer) > 10:
                if not any(word in answer.lower() for word in ['cooler cooler', 'no idea', 'guess']):
                    return {"response": answer, "agent": "general_huggingface"}
        
        answer = self.smart_fallback.get_smart_response(message)
        return {"response": answer, "agent": "general_smart_fallback_final"}
