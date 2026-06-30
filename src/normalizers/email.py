"""
Email Normalizer.

Responsibilities
----------------
- Remove whitespace
- Convert to lowercase
- Validate email format
- Remove duplicates
"""

from __future__ import annotations

from pydantic import EmailStr, ValidationError, TypeAdapter

from src.interfaces.normalizer import BaseNormalizer
from src.models.candidate import Candidate
from src.models.intermediate import IntermediateCandidate


class EmailNormalizer(BaseNormalizer):
    """
    Normalize candidate email addresses.
    """

    def normalize(
        self,
        candidate: IntermediateCandidate,
    ) -> Candidate:

        result = Candidate(
            candidate_id=candidate.candidate_id,
            full_name=candidate.full_name,
            headline=candidate.headline,
            years_experience=candidate.years_experience,
        )

        adapter = TypeAdapter(EmailStr)

        emails: list[EmailStr] = []
        seen: set[str] = set()

        for email in candidate.emails:

            if not email:
                continue

            email = email.strip().lower()

            try:
                normalized = adapter.validate_python(email)

                key = str(normalized)

                if key not in seen:
                    seen.add(key)
                    emails.append(normalized)

            except ValidationError:
                continue

        result.emails = emails

        return result