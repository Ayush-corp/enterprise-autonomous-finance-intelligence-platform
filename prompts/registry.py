from __future__ import annotations

from prompts.base import PromptTemplate
from prompts.types import PromptName


class PromptRegistry:

    def __init__(self) -> None:
        self._registry: dict[str, PromptTemplate] = {}

    def register(
        self,
        prompt: PromptTemplate,
    ) -> None:
        self._registry[prompt.name] = prompt

    def get(
        self,
        name: PromptName,
    ) -> PromptTemplate:
        return self._registry[name]