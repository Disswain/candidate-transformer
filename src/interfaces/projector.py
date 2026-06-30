"""
Base Projector Interface
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from src.models.candidate import Candidate


class BaseProjector(ABC):

    @abstractmethod
    def project(
        self,
        candidate: Candidate,
    ) -> dict:
        raise NotImplementedError