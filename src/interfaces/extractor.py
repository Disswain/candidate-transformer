"""
Base Extractor Interface

Every extractor must implement this interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.models.candidate import Candidate


class BaseExtractor(ABC):
    """
    Abstract base class for all extractors.
    """

    @abstractmethod
    def extract(self, source: str) -> list[Candidate]:
        """
        Extract candidate(s) from a source.

        Parameters
        ----------
        source : str
            Path or URL of the data source.

        Returns
        -------
        list[Candidate]
        """
        raise NotImplementedError