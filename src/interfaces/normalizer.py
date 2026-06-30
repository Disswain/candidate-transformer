"""
Base Normalizer Interface
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.models.intermediate import IntermediateCandidate


class BaseNormalizer(ABC):
    """
    Base class for all normalizers.
    """

    @abstractmethod
    def normalize(
        self,
        candidate: IntermediateCandidate,
    ) -> IntermediateCandidate:
        """
        Normalize a candidate.

        Returns the same candidate after modification.
        """
        raise NotImplementedError