"""
Location Normalizer.

Responsibilities
----------------
- Normalize country names
- Convert country to ISO-3166 alpha-2
- Trim whitespace
- Proper case city/region
- Never raise exceptions
"""

from __future__ import annotations

import pycountry

from src.interfaces.normalizer import BaseNormalizer
from src.models.candidate import Candidate
from src.models.intermediate import IntermediateCandidate
from src.models.location import Location


class LocationNormalizer(BaseNormalizer):
    """
    Normalize candidate location.
    """

    COUNTRY_ALIASES = {
        "india": "IN",
        "ind": "IN",
        "republic of india": "IN",

        "united states": "US",
        "usa": "US",
        "u.s.a": "US",

        "united kingdom": "GB",
        "uk": "GB",
        "great britain": "GB",
    }

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
            phones=candidate.phones,
        )

        city = self._clean(candidate.city)
        region = self._clean(candidate.region)
        country = self._normalize_country(
            candidate.country
        )

        result.location = Location(
            city=city,
            region=region,
            country=country,
        )

        return result

    # -----------------------------------------------------

    @staticmethod
    def _clean(
        value: str | None,
    ) -> str | None:

        if value is None:
            return None

        value = value.strip()

        if not value:
            return None

        return value.title()

    # -----------------------------------------------------

    def _normalize_country(
        self,
        country: str | None,
    ) -> str | None:

        if not country:
            return None

        country = country.strip()

        if not country:
            return None

        lower = country.lower()

        if lower in self.COUNTRY_ALIASES:
            return self.COUNTRY_ALIASES[lower]

        try:

            match = pycountry.countries.lookup(country)

            return match.alpha_2

        except LookupError:

            return None