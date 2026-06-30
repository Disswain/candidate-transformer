"""
LinkedIn Profile Extractor

Reads LinkedIn JSON and converts it into an
IntermediateCandidate.

No normalization.
No validation.
No merging.
"""

from __future__ import annotations

from src.interfaces.extractor import BaseExtractor
from src.models.intermediate import IntermediateCandidate
from src.utils.constants import SOURCE_LINKEDIN
from src.utils.file_loader import FileLoader
from src.utils.logger import logger


class LinkedInParser(BaseExtractor):

    def extract(
        self,
        source: str,
    ) -> list[IntermediateCandidate]:

        logger.info("Reading LinkedIn profile %s", source)

        data = FileLoader.load_json(source)

        location = data.get("location", {})

        candidate = IntermediateCandidate(

            source=SOURCE_LINKEDIN,

            full_name=data.get("name"),

            emails=[
                data["email"]
            ] if data.get("email") else [],

            phones=[
                data["phone"]
            ] if data.get("phone") else [],

            city=location.get("city"),

            region=location.get("region"),

            country=location.get("country"),

            linkedin=data.get("profile_url"),

            github=data.get("github_url"),

            portfolio=data.get("portfolio"),

            other_links=data.get(
                "other_links",
                [],
            ),

            headline=data.get("headline"),

            skills=data.get(
                "skills",
                [],
            ),

            experience=data.get(
                "experience",
                [],
            ),

            education=data.get(
                "education",
                [],
            ),
        )

        logger.info("LinkedIn parsed successfully.")

        return [candidate]