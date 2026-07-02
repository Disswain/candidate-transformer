"""
Base Profile Parser.

Shared functionality for profile-based extractors such as:
- LinkedIn
- GitHub
- Resume TXT
- Resume PDF

Responsibilities:
- Safe dictionary access
- List conversion
- Candidate creation
- Shared parsing helpers

This class DOES NOT perform normalization.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from src.interfaces.extractor import BaseExtractor
from src.mappers.education_mapper import EducationMapper
from src.mappers.experience_mapper import ExperienceMapper
from src.mappers.skill_mapper import SkillMapper
from src.models.intermediate import IntermediateCandidate

class BaseProfileParser(BaseExtractor, ABC):
    """
    Base class for all profile parsers.
    """

    @staticmethod
    def safe_get(
        data: dict[str, Any],
        *keys: str,
        default: Any = None,
    ) -> Any:
        """
        Safely access nested dictionaries.

        Example: safe_get(data, "contact", "email")
        """

        value: Any = data

        for key in keys:

            if not isinstance(value, dict):
                return default

            value = value.get(key)

            if value is None:
                return default

        return value

    @staticmethod
    def ensure_list(value: Any) -> list[Any]:
        """
        Convert a value into a list.
        """

        if value is None:
            return []

        if isinstance(value, list):
            return value

        return [value]

    def build_candidate(
        self,
        *,
        source: str,
        data: dict[str, Any],
        metadata: dict[str, Any] | None = None,
    ) -> IntermediateCandidate:
        """
        Build an IntermediateCandidate from a profile dictionary.
        """

        location = self.safe_get(
            data,
            "location",
            default={},
        )

        links = self.safe_get(
            data,
            "links",
            default={},
        )

        return IntermediateCandidate(
            source=source,

            candidate_id=(
                data.get("candidate_id")
                or data.get("id")
            ),

            full_name=(
                data.get("full_name")
                or data.get("name")
            ),

            headline=data.get("headline"),

            years_experience=data.get(
                "years_experience"
            ),

            emails=[
                str(email)
                for email in self.ensure_list(
                    self.safe_get(
                        data,
                        "contact",
                        "emails",
                        default=data.get("emails"),
                    )
                    or self.safe_get(
                        data,
                        "contact",
                        "email",
                        default=data.get("email"),
                    )
                )
                if email
            ],

            phones=[
                str(phone)
                for phone in self.ensure_list(
                    self.safe_get(
                        data,
                        "contact",
                        "phones",
                        default=data.get("phones"),
                    )
                    or self.safe_get(
                        data,
                        "contact",
                        "phone",
                        default=data.get("phone"),
                    )
                )
                if phone
            ],

            city=location.get("city"),

            region=location.get("region"),

            country=location.get("country"),

            linkedin=links.get("linkedin")
            or data.get("linkedin"),

            github=links.get("github")
            or data.get("github"),

            portfolio=links.get("portfolio")
            or data.get("portfolio"),

            other_links=links.get(
                "other",
                [],
            ),

            skills=SkillMapper.from_value(
                data.get("skills")
            ),

            experience=ExperienceMapper.from_value(
                data.get("experience")
            ),

            education=EducationMapper.from_value(
                data.get("education")
            ),

            metadata=metadata or {},
        )

    @abstractmethod
    def extract(
        self,
        source: str,
    ) -> list[IntermediateCandidate]:
        """
        Extract profile data.
        """
        raise NotImplementedError