"""
Education Normalizer.

Responsibilities
----------------
- Canonicalize degree names
- Trim whitespace
- Remove duplicate education records
"""

from __future__ import annotations

from src.interfaces.normalizer import BaseNormalizer
from src.models.candidate import Candidate
from src.models.education import Education
from src.models.intermediate import IntermediateCandidate


class EducationNormalizer(BaseNormalizer):
    """
    Normalize education records.
    """

    DEGREE_MAP = {
        "b.sc": "Bachelor of Science",
        "bsc": "Bachelor of Science",
        "bachelor of science": "Bachelor of Science",

        "m.sc": "Master of Science",
        "msc": "Master of Science",
        "master of science": "Master of Science",

        "b.tech": "Bachelor of Technology",
        "btech": "Bachelor of Technology",
        "bachelor of technology": "Bachelor of Technology",

        "m.tech": "Master of Technology",
        "mtech": "Master of Technology",
        "master of technology": "Master of Technology",

        "ph.d": "Doctor of Philosophy",
        "phd": "Doctor of Philosophy",
        "doctor of philosophy": "Doctor of Philosophy",

        "mba": "Master of Business Administration",
    }

    def normalize(
        self,
        candidate: IntermediateCandidate,
    ) -> Candidate:

        result = Candidate()

        normalized = []
        seen = set()

        for edu in candidate.education:

            institution = (edu.get("institution") or "").strip()

            degree = (edu.get("degree") or "").strip()

            field = (edu.get("field") or "").strip()

            start = edu.get("start_date")
            end = edu.get("end_date")

            canonical_degree = self.DEGREE_MAP.get(
                degree.lower(),
                degree,
            )

            key = (
                institution.lower(),
                canonical_degree.lower(),
                (field or "").lower(),
                start,
                end,
            )

            if key in seen:
                continue

            seen.add(key)

            normalized.append(
                Education(
                    institution=institution or None,
                    degree=canonical_degree or None,
                    field=field or None,
                    start_date=start,
                    end_date=end,
                )
            )

        result.education = normalized

        return result