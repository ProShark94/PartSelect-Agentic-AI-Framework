"""Wrapper around the Deepseek language model API.

This agent calls the Deepseek API in a manner similar to the OpenAI API.
The actual endpoint and request format may differ; consult the Deepseek
documentation for details. If ``DEEPSEEK_API_KEY`` is not set or the
request fails, ``call`` returns ``None``.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

import requests


class DeepSeekAgent:
    """Call the Deepseek language model API."""

    def __init__(self, model: str = "deepseek-chat") -> None:
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.model = model
        # Placeholder endpoint; replace with actual Deepseek endpoint
        self.endpoint = "https://api.deepseek.com/v1/chat/completions"

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