from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class PromptTemplate:
    name: str
    version: str
    system_prompt: str

    def render(self, **kwargs) -> str:
        return self.system_prompt.format(**kwargs)