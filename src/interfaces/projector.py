"""
Base Projector Interface.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from src.models.candidate import Candidate


class BaseProjector(ABC):
    """
    Projects the canonical candidate into the
    configured output schema.
    """

    @abstractmethod
    def project(
        self,
        candidate: Candidate,
    ) -> dict[str, Any]:
        """
        Produce the final output dictionary.
        """
        raise NotImplementedError