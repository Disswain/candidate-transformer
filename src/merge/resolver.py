"""
Candidate Merge Resolver.

Merges multiple canonical Candidate objects into one.

Merge Priority:
Recruiter CSV
ATS
LinkedIn
GitHub
Resume PDF
Resume TXT
"""

from __future__ import annotations
from rapidfuzz import fuzz
from src.models.candidate import Candidate
from src.models.education import Education
from src.models.experience import Experience
from src.models.links import Links
from src.models.skill import Skill
from src.utils.constants import SOURCE_PRIORITY

class MergeResolver:
    """
    Merge multiple Candidate objects.
    """

    def merge(
        self,
        candidates: list[Candidate],
    ) -> Candidate:

        if not candidates:
            return Candidate()

        merged = Candidate()

        ordered = sorted(
            candidates,
            key=self._priority,
        )

        # Identity-

        merged.candidate_id = self._first(
            ordered,
            "candidate_id",
        )

        merged.full_name = self._merge_name(
            ordered,
        )

        merged.headline = self._first(
            ordered,
            "headline",
        )

        merged.years_experience = self._first(
            ordered,
            "years_experience",
        )

       
        # Contact-

        merged.emails = self._unique(
            ordered,
            "emails",
        )

        merged.phones = self._unique(
            ordered,
            "phones",
        )

        
        # Location-
        

        merged.location = self._merge_location(
            ordered,
        )

        # Links-

        merged.links = self._merge_links(
            ordered,
        )

        # Skills-

        merged.skills = self._merge_skills(
            ordered,
        )

        # Experience-

        merged.experience = self._merge_experience(
            ordered,
        )

        # Education-

        merged.education = self._merge_education(
            ordered,
        )

       
        # Provenance-

        seen = set()

        for candidate in ordered:

            for item in candidate.provenance:

                key = (
                    item.field,
                    item.source,
                    item.method,
                )

                if key not in seen:
                    seen.add(key)
                    merged.provenance.append(item)

        return merged

    # =========================================================

    @staticmethod
    def _priority(
        candidate: Candidate,
    ) -> int:

        if not candidate.provenance:
            return len(SOURCE_PRIORITY)

        source = candidate.provenance[0].source

        try:
            return SOURCE_PRIORITY.index(source)
        except ValueError:
            return len(SOURCE_PRIORITY)

    # =========================================================

    @staticmethod
    def _first(
        candidates: list[Candidate],
        field: str,
    ):

        for candidate in candidates:

            value = getattr(
                candidate,
                field,
            )

            if value:
                return value

        return None

    # =========================================================

    @staticmethod
    def _unique(
        candidates: list[Candidate],
        field: str,
    ) -> list:

        values = []
        seen = set()

        for candidate in candidates:

            for value in getattr(candidate, field):

                if value is None:
                    continue

                value = str(value).strip()

                if not value:
                    continue

                if value not in seen:
                    seen.add(value)
                    values.append(value)

        return values

    # =========================================================

    @staticmethod
    def _merge_name(
        candidates: list[Candidate],
    ) -> str | None:

        names = [
            c.full_name
            for c in candidates
            if c.full_name
        ]

        if not names:
            return None

        best = names[0]

        for name in names[1:]:

            if fuzz.ratio(
                best.lower(),
                name.lower(),
            ) > 90:
                continue

        return best

    # =========================================================

    @staticmethod
    def _merge_location(
        candidates: list[Candidate],
    ):

        for candidate in candidates:

            if (
                candidate.location.city
                or candidate.location.region
                or candidate.location.country
            ):
                return candidate.location

        return candidates[0].location

    # =========================================================

    @staticmethod
    def _merge_links(
        candidates: list[Candidate],
    ) -> Links:

        merged = Links()

        seen = set()

        for candidate in candidates:

            links = candidate.links

            if not merged.linkedin and links.linkedin:
                merged.linkedin = links.linkedin

            if not merged.github and links.github:
                merged.github = links.github

            if not merged.portfolio and links.portfolio:
                merged.portfolio = links.portfolio

            for url in links.other:

                if url in (
                    merged.linkedin,
                    merged.github,
                    merged.portfolio,
                ):
                    continue

                if url not in seen:
                    seen.add(url)
                    merged.other.append(url)

        return merged

    # =========================================================

    @staticmethod
    def _merge_skills(
        candidates: list[Candidate],
    ) -> list[Skill]:

        merged = []
        seen = set()

        for candidate in candidates:

            for skill in candidate.skills:

                key = skill.name.lower()

                if key not in seen:
                    seen.add(key)
                    merged.append(skill)

        merged.sort(
            key=lambda s: s.name.lower()
        )

        return merged

    # =========================================================

    # 
        # =========================================================

    @staticmethod
    def _merge_experience(
        candidates: list[Candidate],
    ) -> list[Experience]:

        merged: list[Experience] = []
        seen: set[tuple] = set()

        for candidate in candidates:

            for exp in candidate.experience:

                key = (
                    (exp.company or "").strip().lower(),
                    (exp.title or "").strip().lower(),
                    exp.start_date,
                    exp.end_date,
                )

                if key in seen:
                    continue

                seen.add(key)
                merged.append(exp)

        return merged

    
    @staticmethod
    def _merge_education(
        candidates: list[Candidate],
    ) -> list[Education]:

        merged: list[Education] = []
        seen: set[tuple] = set()

        DEGREE_MAP = {
            "b.sc": "bachelor of science",
            "bsc": "bachelor of science",
            "bachelor of science": "bachelor of science",

            "m.sc": "master of science",
            "msc": "master of science",
            "master of science": "master of science",

            "b.tech": "bachelor of technology",
            "btech": "bachelor of technology",

            "m.tech": "master of technology",
            "mtech": "master of technology",
        }

        for candidate in candidates:

            for edu in candidate.education:

                institution = (
                    (edu.institution or "")
                    .strip()
                    .lower()
                )

                degree = (
                    (edu.degree or "")
                    .strip()
                    .lower()
                )

                degree = DEGREE_MAP.get(
                    degree,
                    degree,
                )

                field = (
                    (edu.field or "")
                    .strip()
                    .lower()
                )

                key = (
                    institution,
                    degree,
                    field,
                )

                if key in seen:
                    continue

                seen.add(key)
                merged.append(edu)

        return merged