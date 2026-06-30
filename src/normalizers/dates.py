"""
Date Normalizer.

Responsibilities
----------------
- Normalize supported date formats
- Return YYYY-MM or YYYY
- Reject invalid dates
- Reject future dates
- Reject end_date < start_date
"""

from __future__ import annotations

from datetime import datetime

from dateutil import parser

from src.interfaces.normalizer import BaseNormalizer
from src.models.candidate import Candidate
from src.models.education import Education
from src.models.experience import Experience
from src.models.intermediate import IntermediateCandidate


class DateNormalizer(BaseNormalizer):
    """
    Normalize experience and education dates.
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
            phones=candidate.phones,
        )

        result.experience = [
            self._normalize_experience(item)
            for item in candidate.experience
        ]

        result.education = [
            self._normalize_education(item)
            for item in candidate.education
        ]

        return result

    # ---------------------------------------------------------

    def _normalize_experience(
        self,
        item: dict,
    ) -> Experience:

        start = self._normalize_date(
            item.get("start_date")
        )

        end = self._normalize_date(
            item.get("end_date")
        )

        if (
            start
            and end
            and self._compare_dates(start, end)
        ):
            end = None

        return Experience(
            company=item.get("company"),
            title=item.get("title"),
            start_date=start,
            end_date=end,
            description=item.get("description"),
        )

    # ---------------------------------------------------------

    def _normalize_education(
        self,
        item: dict,
    ) -> Education:

        start = self._normalize_date(
            item.get("start_date")
        )

        end = self._normalize_date(
            item.get("end_date")
        )

        if (
            start
            and end
            and self._compare_dates(start, end)
        ):
            end = None

        return Education(
            institution=item.get("institution"),
            degree=item.get("degree"),
            field=item.get("field"),
            start_date=start,
            end_date=end,
        )

    # ---------------------------------------------------------

    @staticmethod
    def _normalize_date(
        value: str | None,
    ) -> str | None:

        if value is None:
            return None

        value = str(value).strip()

        if not value:
            return None

        # Year only
        if (
            len(value) == 4
            and value.isdigit()
        ):
            year = int(value)

            if year > datetime.now().year:
                return None

            return value

        try:

            dt = parser.parse(
                value,
                fuzzy=True,
                default=datetime(1900, 1, 1),
            )

            if dt > datetime.now():
                return None

            # If only a year was supplied, parser defaults month=1.
            # Preserve YYYY if original input looked like only a year.
            if value.isdigit() and len(value) == 4:
                return f"{dt.year}"

            return dt.strftime("%Y-%m")

        except Exception:
            return None

    # ---------------------------------------------------------

    @staticmethod
    def _compare_dates(
        start: str,
        end: str,
    ) -> bool:
        """
        Returns True if end < start.
        """

        try:

            if len(start) == 4:
                start_dt = datetime.strptime(
                    start,
                    "%Y",
                )
            else:
                start_dt = datetime.strptime(
                    start,
                    "%Y-%m",
                )

            if len(end) == 4:
                end_dt = datetime.strptime(
                    end,
                    "%Y",
                )
            else:
                end_dt = datetime.strptime(
                    end,
                    "%Y-%m",
                )

            return end_dt < start_dt

        except Exception:
            return False