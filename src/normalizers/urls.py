"""
URL Normalizer.

Normalizes external profile URLs.
"""

from __future__ import annotations

from urllib.parse import urlparse

from src.interfaces.normalizer import BaseNormalizer
from src.models.candidate import Candidate
from src.models.intermediate import IntermediateCandidate
from src.models.links import Links


class URLNormalizer(BaseNormalizer):

    def normalize(
        self,
        candidate: IntermediateCandidate,
    ) -> Candidate:

        result = Candidate()

        result.links = Links(
            linkedin=self._normalize(candidate.linkedin),
            github=self._normalize(candidate.github),
            portfolio=self._normalize(candidate.portfolio),
            other=[
                self._normalize(url)
                for url in candidate.other_links
                if self._normalize(url)
            ],
        )

        return result

    @staticmethod
    def _normalize(
        url: str | None,
    ) -> str | None:

        if not url:
            return None

        url = url.strip()

        if not url:
            return None

        parsed = urlparse(url)

        if not parsed.scheme:
            url = "https://" + url

        return url