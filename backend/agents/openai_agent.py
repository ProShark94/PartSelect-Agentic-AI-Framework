"""Wrapper around the OpenAI ChatCompletion endpoint.

This agent makes HTTP requests to the OpenAI API to generate answers. The
implementation expects an ``OPENAI_API_KEY`` environment variable. If the
key is not available or the request fails, the ``call`` method returns
``None`` so that the orchestrator can fall back to other agents.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

import requests


class OpenAIAgent:
    """Call the OpenAI Chat API to obtain a response."""

    def __init__(self, model: str = "gpt-3.5-turbo") -> None:
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.endpoint = "https://api.openai.com/v1/chat/completions"

    def call(self, prompt: str) -> Optional[str]:
        if not self.api_key:
            return None
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant specialised in appliance parts."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }
        try:
            response = requests.post(self.endpoint, headers=headers, data=json.dumps(payload), timeout=10)
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
        except Exception:
            pass
        return None