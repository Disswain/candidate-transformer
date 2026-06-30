"""
Confidence Calculator.

Calculates confidence scores for every major field
and an overall confidence score.

Higher confidence is assigned to data originating
from more reliable sources.

Source Priority
---------------
Recruiter CSV
ATS
LinkedIn
GitHub
Resume PDF
Resume TXT
"""

from __future__ import annotations

from statistics import mean

from src.models.candidate import Candidate
from src.models.confidence import Confidence


class ConfidenceCalculator:
    """
    Calculates confidence values.
    """

    DEFAULT_WEIGHTS = {
        "full_name": 1.0,
        "emails": 0.95,
        "phones": 0.95,
        "location": 0.90,
        "headline": 0.85,
        "years_experience": 0.90,
        "skills": 0.90,
        "experience": 0.90,
        "education": 0.90,
        "links": 0.80,
    }

    # ---------------------------------------------------------

    def calculate(
        self,
        candidate: Candidate,
    ) -> Confidence:

        confidence = Confidence()

        confidence.full_name = self._score(
            candidate.full_name,
            self.DEFAULT_WEIGHTS["full_name"],
        )

        confidence.emails = self._score(
            candidate.emails,
            self.DEFAULT_WEIGHTS["emails"],
        )

        confidence.phones = self._score(
            candidate.phones,
            self.DEFAULT_WEIGHTS["phones"],
        )

        confidence.location = self._score(
            candidate.location.country
            or candidate.location.city,
            self.DEFAULT_WEIGHTS["location"],
        )

        confidence.headline = self._score(
            candidate.headline,
            self.DEFAULT_WEIGHTS["headline"],
        )

        confidence.years_experience = self._score(
            candidate.years_experience,
            self.DEFAULT_WEIGHTS["years_experience"],
        )

        confidence.skills = self._score(
            candidate.skills,
            self.DEFAULT_WEIGHTS["skills"],
        )

        confidence.experience = self._score(
            candidate.experience,
            self.DEFAULT_WEIGHTS["experience"],
        )

        confidence.education = self._score(
            candidate.education,
            self.DEFAULT_WEIGHTS["education"],
        )

        confidence.links = self._score(
            (
                candidate.links.linkedin
                or candidate.links.github
                or candidate.links.portfolio
            ),
            self.DEFAULT_WEIGHTS["links"],
        )

        confidence.overall = round(
            mean(
                [
                    confidence.full_name,
                    confidence.emails,
                    confidence.phones,
                    confidence.location,
                    confidence.headline,
                    confidence.years_experience,
                    confidence.skills,
                    confidence.experience,
                    confidence.education,
                    confidence.links,
                ]
            ),
            2,
        )

        return confidence

    # ---------------------------------------------------------

    @staticmethod
    def _score(
        value,
        weight: float,
    ) -> float:
        """
        Assign a confidence score.

        If the field is populated, return its configured weight.
        Otherwise return 0.
        """

        if value is None:
            return 0.0

        if isinstance(value, str):
            if not value.strip():
                return 0.0

        if isinstance(value, (list, tuple, set)):
            if len(value) == 0:
                return 0.0

        return round(weight, 2)