"""
Name Normalizer.

Responsibilities
----------------
- Remove prefixes
- Collapse whitespace
- Normalize initials
- Proper case
- Unicode safe
- Never fail
"""

from __future__ import annotations

import re

from src.interfaces.normalizer import BaseNormalizer
from src.models.candidate import Candidate
from src.models.intermediate import IntermediateCandidate
from src.utils.constants import NAME_PREFIXES


class NameNormalizer(BaseNormalizer):
    """
    Normalize candidate names.
    """

    _SPACE_PATTERN = re.compile(r"\s+")
    _DOT_PATTERN = re.compile(r"\.")

    def normalize(
        self,
        candidate: IntermediateCandidate,
    ) -> Candidate:

        name = candidate.full_name

        if not name:

            return Candidate()

        name = self._SPACE_PATTERN.sub(
            " ",
            name.strip(),
        )

        name = self._DOT_PATTERN.sub(
            "",
            name,
        )

        parts = []

        for token in name.split():

            lower = token.lower()

            if lower in NAME_PREFIXES:
                continue

            if len(token) == 1:
                parts.append(token.upper())
            else:
                parts.append(token.capitalize())

        normalized = " ".join(parts)

        return Candidate(
            candidate_id=candidate.candidate_id,
            full_name=normalized,
            headline=candidate.headline,
            years_experience=candidate.years_experience,
        )