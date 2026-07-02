"""
Base Normalizer Interface.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from src.models.candidate import Candidate
from src.models.intermediate import IntermediateCandidate

class BaseNormalizer(ABC):
    """
    Converts an IntermediateCandidate into a Candidate.
    """

    @abstractmethod
    def normalize(
        self,
        candidate: IntermediateCandidate,
    ) -> Candidate:
        """
        Normalize extracted candidate data.

        Returns-
        Candidate
        """
        raise NotImplementedError