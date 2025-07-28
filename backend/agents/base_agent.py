"""Abstract base class for all agents.

Each agent implements a `handle` method that takes a user query and a
context dictionary and returns a response dictionary. Agents can update
the context to maintain state across invocations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseAgent(ABC):
    """Defines the interface for an agent."""

    @abstractmethod
    def handle(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process a query and optionally update the context.

        Args:
            query: The user’s message.
            context: Shared state for the current conversation. Agents
                can read from and write to this dictionary.

        Returns:
            A dictionary containing at least a ``response`` field with the
            agent’s answer and optionally other metadata.
        """
        raise NotImplementedError