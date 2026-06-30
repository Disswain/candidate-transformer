"""
Name Normalizer

Responsibilities

✓ Trim whitespace
✓ Remove prefixes
✓ Collapse spaces
✓ Handle initials
✓ Proper casing
✓ Unicode safe
"""

from __future__ import annotations

import re

from src.interfaces.normalizer import BaseNormalizer
from src.models.intermediate import IntermediateCandidate


PREFIXES = (
    "mr",
    "mrs",
    "ms",
    "dr",
    "prof",
)


class NameNormalizer(BaseNormalizer):

    def normalize(
        self,
        candidate: IntermediateCandidate,
    ) -> IntermediateCandidate:

        if not candidate.full_name:
            return candidate

        name = candidate.full_name.strip()

        # Collapse whitespace
        name = re.sub(r"\s+", " ", name)

        # Remove dots from initials
        name = name.replace(".", "")

        parts = name.split()

        # Remove prefixes
        while parts and parts[0].lower() in PREFIXES:
            parts.pop(0)

        cleaned = []

        for part in parts:

            if len(part) == 1:
                cleaned.append(part.upper())

            else:
                cleaned.append(part.capitalize())

        candidate.full_name = " ".join(cleaned)

        return candidate