"""
Base Merger Interface
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.models.candidate import Candidate


class BaseMerger(ABC):

    @abstractmethod
    def merge(
        self,
        candidates: list[Candidate],
    ) -> Candidate:
        raise NotImplementedError