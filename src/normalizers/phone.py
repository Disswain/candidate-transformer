"""
Phone Normalizer.

Responsibilities
----------------
- Remove whitespace
- Validate phone numbers
- Convert to E.164 format
- Remove duplicates
- Ignore invalid numbers
"""

from __future__ import annotations

import phonenumbers

from src.interfaces.normalizer import BaseNormalizer
from src.models.candidate import Candidate
from src.models.intermediate import IntermediateCandidate
from src.utils.constants import DEFAULT_COUNTRY


class PhoneNormalizer(BaseNormalizer):
    """
    Normalize candidate phone numbers.
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
            emails=candidate.emails,
        )

        phones: list[str] = []
        seen: set[str] = set()

        for phone in candidate.phones:

            if phone is None:
                continue

            phone = str(phone).strip()

            if not phone:
                continue

            try:

                parsed = phonenumbers.parse(
                    phone,
                    DEFAULT_COUNTRY,
                )

                if not phonenumbers.is_valid_number(parsed):
                    continue

                normalized = phonenumbers.format_number(
                    parsed,
                    phonenumbers.PhoneNumberFormat.E164,
                )

                if normalized not in seen:
                    seen.add(normalized)
                    phones.append(normalized)

            except phonenumbers.NumberParseException:
                continue

        result.phones = phones

        return result