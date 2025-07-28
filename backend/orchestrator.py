"""Orchestrator for routing user messages to specialised agents."""

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
    """Coordinates multiple agents to answer user queries."""

    def __init__(self) -> None:
        # Instantiate language model agents first
        self.product_agent = ProductSearchAgent(use_vector=True)
        self.compatibility_agent = CompatibilityAgent(self.product_agent)
        # Instantiate OpenAI and Deepseek agents for use across the system
        self.openai_agent = OpenAIAgent()
        self.deepseek_agent = DeepSeekAgent()
        
        # Add working HuggingFace agent and smart fallback
        try:
            self.huggingface_agent = WorkingHuggingFaceAgent()
            print("DEBUG: WorkingHuggingFaceAgent loaded successfully")
        except Exception as e:
            print(f"DEBUG: Failed to load WorkingHuggingFaceAgent: {e}")
            self.huggingface_agent = None
            
        # Initialize smart fallback system
        self.smart_fallback = SmartFallbackSystem()
        
        # Choose an intent classifier: prefer LLM classifier if at least one API key is available
        try:
            from agents.llm_intent_classifier import LLMIntentClassifier  # type: ignore
            if self.openai_agent.api_key or self.deepseek_agent.api_key:
                self.intent_classifier = LLMIntentClassifier(
                    openai_agent=self.openai_agent,
                    deepseek_agent=self.deepseek_agent,
                )
                print("DEBUG: Using LLM Intent Classifier")
            else:
                self.intent_classifier = IntentClassifier()
                print("DEBUG: Using basic keyword Intent Classifier")
        except Exception as e:
            print(f"DEBUG: Failed to load LLM classifier: {e}")
            self.intent_classifier = IntentClassifier()
            
        self.installation_agent = InstallationAgent(
            product_agent=self.product_agent,
            openai_agent=self.openai_agent,
            deepseek_agent=self.deepseek_agent,
        )
        self.order_support_agent = OrderSupportAgent()

    def handle_message(self, message: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyse the user message, select the correct agent and return its response.

        Args:
            message: The user's input string.
            context: A dictionary representing conversation context. This can
                include previous messages, identified part numbers, etc. It
                will be updated in place.

        Returns:
            A dictionary containing the agent's response and metadata.
        """
        # Add message to context history
        history: List[Dict[str, str]] = context.setdefault("history", [])
        history.append({"role": "user", "content": message})

        # Determine intent
        intent_result = self.intent_classifier.handle(message, context)
        intent = intent_result.get("intent")
        print(f"DEBUG: Intent classified as: {intent}")

        if intent == "product_info":
            result = self.product_agent.handle(message, context)
        elif intent == "compatibility":
            result = self.compatibility_agent.handle(message, context)
        elif intent == "installation" and any(word in message.lower() for word in ['install', 'replace part', 'how to install', 'installation guide']):
            # Only use installation agent for actual installation requests
            result = self.installation_agent.handle(message, context)
        elif intent == "order_support" and any(word in message.lower() for word in ['order', 'delivery', 'shipping', 'tracking']):
            # Only use order support for actual order-related queries
            result = self.order_support_agent.handle(message, context)
        else:  # general query - includes troubleshooting, part questions, etc.
            # Try available AI models in order: OpenAI -> Deepseek -> HuggingFace -> Smart Fallback
            prompt = (
                "You are an assistant for an e‑commerce appliance parts site. "
                "Answer the following question in a concise, friendly manner: "
                f"{message}"
            )
            print(f"DEBUG: Calling AI models with prompt: {prompt[:100]}...")
            
            answer = None
            used_model = "none"
            
            # Try OpenAI first
            answer = self.openai_agent.call(prompt)
            if answer and answer.strip() and "error" not in answer.lower():
                used_model = "openai"
                print(f"DEBUG: OpenAI response: {answer[:100]}...")
            else:
                print("DEBUG: OpenAI failed, trying Deepseek...")
                # Try Deepseek
                answer = self.deepseek_agent.call(prompt)
                if answer and answer.strip() and "error" not in answer.lower():
                    used_model = "deepseek"
                    print(f"DEBUG: Deepseek response: {answer[:100]}...")
                else:
                    print("DEBUG: Deepseek failed, trying smart fallback first...")
                    # Try smart fallback before unreliable HuggingFace model
                    answer = self.smart_fallback.get_smart_response(message)
                    if answer and answer.strip() and len(answer) > 20:
                        used_model = "smart_fallback"
                        print(f"DEBUG: Smart fallback response: {answer[:100]}...")
                    else:
                        print("DEBUG: Smart fallback didn't find match, trying HuggingFace...")
                        # Try HuggingFace as last resort
                        if self.huggingface_agent and self.huggingface_agent.is_available():
                            answer = self.huggingface_agent.call(message)
                            if answer and answer.strip() and len(answer) > 10 and not any(word in answer.lower() for word in ['cooler cooler', 'no idea', 'guess']):
                                used_model = "huggingface"
                                print(f"DEBUG: HuggingFace response: {answer[:100]}...")
                            else:
                                # HuggingFace failed or gave bad response, use smart fallback
                                answer = self.smart_fallback.get_smart_response(message)
                                used_model = "smart_fallback_final"
                                print(f"DEBUG: Using smart fallback after HuggingFace failed: {answer[:100]}...")
            
            if not answer or not answer.strip():
                print("DEBUG: All methods failed, using smart fallback system")
                answer = self.smart_fallback.get_smart_response(message)
                used_model = "smart_fallback_emergency"
                print(f"DEBUG: Emergency fallback response: {answer[:100]}...")
            
            result = {"response": answer, "agent": f"general_{used_model}"}

        # Append agent response to history for context
        history.append({"role": "assistant", "content": str(result.get("response"))})
        return result
