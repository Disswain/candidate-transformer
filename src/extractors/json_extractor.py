"""
ATS JSON Extractor.

Reads ATS JSON exports and converts them into
IntermediateCandidate objects.

Responsibilities
----------------
- Read JSON
- Support single candidate object
- Support list of candidates
- Handle nested contact/location fields
- Ignore unknown fields
- Never normalize
- Never merge
"""

from __future__ import annotations

from typing import Any

from src.interfaces.extractor import BaseExtractor
from src.models.intermediate import IntermediateCandidate
from src.utils.constants import SOURCE_ATS
from src.utils.file_loader import FileLoader
from src.utils.logger import get_logger

logger = get_logger(__name__)


class JSONExtractor(BaseExtractor):
    """
    Extract candidates from ATS JSON.
    """

    def extract(
        self,
        source: str,
    ) -> list[IntermediateCandidate]:

        logger.info("Reading ATS JSON: %s", source)

        data = FileLoader.read_json(source)

        records = self._resolve_records(data)

        candidates: list[IntermediateCandidate] = []

        for index, record in enumerate(records):

            try:
                candidates.append(
                    self._parse_candidate(record)
                )

            except Exception as exc:

                logger.exception(
                    "Failed parsing candidate %d: %s",
                    index,
                    exc,
                )

        logger.info(
            "Successfully extracted %d candidate(s).",
            len(candidates),
        )

        return candidates

    # --------------------------------------------------

    @staticmethod
    def _resolve_records(
        data: Any,
    ) -> list[dict[str, Any]]:
        """
        Accept common ATS export formats.

        Supported:

        {
            "candidate": {...}
        }

        {
            "candidates": [...]
        }

        [
            {...},
            {...}
        ]
        """

        if isinstance(data, list):
            return data

        if not isinstance(data, dict):
            raise ValueError("Unsupported JSON structure.")

        if "candidates" in data:
            return data["candidates"]

        if "candidate" in data:
            return [data["candidate"]]

        return [data]

    # --------------------------------------------------

    @staticmethod
    def _parse_candidate(
        record: dict[str, Any],
    ) -> IntermediateCandidate:

        contact = record.get("contact", {})
        location = record.get("location", {})
        links = record.get("links", {})

        emails = JSONExtractor._ensure_list(
            contact.get("emails")
            or contact.get("email")
        )

        phones = JSONExtractor._ensure_list(
            contact.get("phones")
            or contact.get("phone")
        )

        skills = JSONExtractor._ensure_list(
            record.get("skills")
        )

        return IntermediateCandidate(

            source=SOURCE_ATS,

            candidate_id=record.get("candidate_id"),

            full_name=record.get("full_name")
            or record.get("name"),

            headline=record.get("headline"),

            years_experience=record.get(
                "years_experience"
            ),

            emails=[
                str(email)
                for email in emails
                if email
            ],

            phones=[
                str(phone)
                for phone in phones
                if phone
            ],

            city=location.get("city"),

            region=location.get("region"),

            country=location.get("country"),

            linkedin=links.get("linkedin"),

            github=links.get("github"),

            portfolio=links.get("portfolio"),

            other_links=links.get(
                "other",
                [],
            ),

            skills=skills,

            experience=record.get(
                "experience",
                [],
            ),

            education=record.get(
                "education",
                [],
            ),

            metadata={
                "raw_record": record
            },
        )

    # --------------------------------------------------

    @staticmethod
    def _ensure_list(
        value: Any,
    ) -> list[Any]:

        if value is None:
            return []

        if isinstance(value, list):
            return value

        return [value]