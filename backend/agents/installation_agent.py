"""Agent for providing installation and repair instructions."""

from __future__ import annotations

from typing import Any, Dict, Optional

from .base_agent import BaseAgent
from .product_search_agent import ProductSearchAgent
from .openai_agent import OpenAIAgent
from .deepseek_agent import DeepSeekAgent


class InstallationAgent(BaseAgent):
    """Provide installation or repair instructions for a part or general issue."""

    def __init__(
        self,
        product_agent: Optional[ProductSearchAgent] = None,
        openai_agent: Optional[OpenAIAgent] = None,
        deepseek_agent: Optional[DeepSeekAgent] = None,
    ) -> None:
        self.product_agent = product_agent or ProductSearchAgent()
        self.openai_agent = openai_agent or OpenAIAgent()
        self.deepseek_agent = deepseek_agent or DeepSeekAgent()

    def handle(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        # First check if this is a general troubleshooting question
        q = query.lower()
        
        # Ice maker troubleshooting
        if any(keyword in q for keyword in ["ice maker", "ice", "icemaker"]):
            response = (
                "Here are common ice maker troubleshooting steps:\n\n"
                "1. **Check Power**: Ensure the ice maker is turned ON (switch usually inside freezer)\n"
                "2. **Water Supply**: Verify water line is connected and water filter isn't clogged\n"
                "3. **Reset**: Turn ice maker OFF for 24 hours, then back ON\n"
                "4. **Temperature**: Freezer should be 0-5°F for proper ice production\n"
                "5. **Water Filter**: Replace if older than 6 months (part WP12345 for most Whirlpool models)\n\n"
                "If these steps don't help, you may need to replace the ice maker assembly. "
                "What's your refrigerator model number? I can find the right replacement part."
            )
            return {"response": response, "agent": "installation"}
        
        # General refrigerator issues
        elif any(keyword in q for keyword in ["refrigerator", "fridge", "freezer"]) and not any(part_word in q for part_word in ["part", "install", "replace"]):
            response = (
                "I can help troubleshoot refrigerator issues! Common problems include:\n\n"
                "• **Not cooling**: Check temperature settings, clean coils, replace air filter\n"
                "• **Water/ice issues**: Replace water filter, check water line connections\n"
                "• **Noise**: Check for loose parts, level the unit\n"
                "• **Door seals**: Clean gaskets, check for tears\n\n"
                "What specific problem are you experiencing? Also, please share your model number "
                "so I can provide targeted guidance and part recommendations."
            )
            return {"response": response, "agent": "installation"}
        
        # Dishwasher issues
        elif any(keyword in q for keyword in ["dishwasher"]) and not any(part_word in q for part_word in ["part", "install", "replace"]):
            response = (
                "Common dishwasher troubleshooting steps:\n\n"
                "• **Not cleaning well**: Clean spray arms, check water temperature (120°F)\n"
                "• **Not draining**: Clean filter, check garbage disposal\n"
                "• **Leaking**: Inspect door seals, check spray arm connections\n"
                "• **Not starting**: Check door latch, reset circuit breaker\n\n"
                "What's the specific issue you're facing? Your model number would help me "
                "provide more targeted advice and part suggestions."
            )
            return {"response": response, "agent": "installation"}
        
        # Check for specific part installation only if the query mentions installation/install/replace
        elif any(keyword in q for keyword in ["install", "installation", "replace", "how to install"]):
            # Check conversation history for part numbers
            history = context.get("history", [])
            full_conversation = " ".join([msg.get("content", "") for msg in history])
            combined_text = f"{full_conversation} {query}"
            
            # Attempt to extract part number and return installation instructions
            part_match = self.product_agent.PART_PATTERN.search(combined_text)
            if part_match:
                part_number = part_match.group(1)
                item = self.product_agent._find_by_part_number(part_number)
                if item:
                    return {
                        "response": item.get("instructions", item.get("installation")),
                        "agent": "installation",
                        "part_number": part_number,
                    }
        
        # If no specific appliance mentioned, try using LLMs for general troubleshooting
        prompt = (
            "You are a repair assistant specialised in refrigerators and dishwashers. "
            "Provide concise troubleshooting steps for the following problem: "
            f"{query}"
        )
        # Try OpenAI first
        answer = self.openai_agent.call(prompt)
        if not answer:
            answer = self.deepseek_agent.call(prompt)
        
        if answer:
            return {"response": answer, "agent": "installation"}
        else:
            # Enhanced fallback for installation/repair queries
            return {
                "response": (
                    "I'd be happy to help with installation or troubleshooting! "
                    "For the best assistance, please provide:\n\n"
                    "1. **Appliance type** (refrigerator, dishwasher, etc.)\n"
                    "2. **Model number** (usually on a sticker inside the door)\n"
                    "3. **Specific issue** you're experiencing\n"
                    "4. **Part number** (if you have a specific part in mind)\n\n"
                    "This information helps me provide accurate troubleshooting steps and "
                    "recommend the right replacement parts if needed."
                ),
                "agent": "installation"
            }