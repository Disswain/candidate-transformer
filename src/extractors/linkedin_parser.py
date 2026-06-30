"""
LinkedIn Profile Extractor.

Reads a LinkedIn profile JSON file and converts it into an
IntermediateCandidate.

Responsibilities
----------------
- Read LinkedIn JSON
- Extract candidate fields
- Never normalize
- Never merge
- Return IntermediateCandidate
"""

from __future__ import annotations

from src.extractors.base_profile_parser import BaseProfileParser
from src.models.intermediate import IntermediateCandidate
from src.utils.constants import SOURCE_LINKEDIN
from src.utils.file_loader import FileLoader
from src.utils.logger import get_logger

logger = get_logger(__name__)


class LinkedInParser(BaseProfileParser):
    """
    LinkedIn profile extractor.
    """

    def extract(
        self,
        source: str,
    ) -> list[IntermediateCandidate]:

        logger.info("Reading LinkedIn profile: %s", source)

        data = FileLoader.read_json(source)

        # Some LinkedIn exports wrap the profile
        if "profile" in data and isinstance(data["profile"], dict):
            data = data["profile"]

        candidate = self.build_candidate(
            source=SOURCE_LINKEDIN,
            data=data,
            metadata={
                "source_file": source,
                "parser": "linkedin",
            },
        )

        logger.info(
            "Successfully extracted LinkedIn profile."
        )

        return [candidate]