"""
Base Merger Interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.models.candidate import Candidate


class BaseMerger(ABC):
    """
    Merges multiple Candidate objects into one canonical profile.
    """

    @abstractmethod
    def merge(
        self,
        candidates: list[Candidate],
    ) -> Candidate:
        """
        Merge multiple normalized candidates.
        """
        raise NotImplementedError