"""
Base Extractor Interface.

Every extractor converts an external source into one or more
IntermediateCandidate objects.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from src.models.intermediate import IntermediateCandidate

class BaseExtractor(ABC):
    """
    Abstract base class for all extractors.
    """

    @abstractmethod
    def extract(
        self,
        source: str,
    ) -> list[IntermediateCandidate]:
        """
        Extract candidate data from a source.

        Parameters-
        source:
            File path or URL.

        Returns-
        list[IntermediateCandidate]
        """
        raise NotImplementedError