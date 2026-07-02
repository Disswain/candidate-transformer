"""
GitHub Profile Extractor.

Reads a GitHub profile JSON export and converts it into an
IntermediateCandidate.

Responsibilities:
- Read GitHub JSON
- Extract candidate fields
- Infer skills from languages/topics (if present)
- Never normalize
- Never merge
"""

from __future__ import annotations
from typing import Any
from src.extractors.base_profile_parser import BaseProfileParser
from src.models.intermediate import IntermediateCandidate
from src.utils.constants import SOURCE_GITHUB
from src.utils.file_loader import FileLoader
from src.utils.logger import get_logger

logger = get_logger(__name__)


class GitHubParser(BaseProfileParser):
    """
    GitHub profile extractor.
    """

    def extract(
        self,
        source: str,
    ) -> list[IntermediateCandidate]:

        logger.info("Reading GitHub profile: %s", source)

        data = FileLoader.read_json(source)

        candidate_data = self._transform(data)

        candidate = self.build_candidate(
            source=SOURCE_GITHUB,
            data=candidate_data,
            metadata={
                "source_file": source,
                "parser": "github",
            },
        )

        logger.info("GitHub profile parsed successfully.")

        return [candidate]
    
    def _transform(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Convert GitHub JSON into the common profile format
        expected by BaseProfileParser.
        """

        skills = []

        # Explicit skills
        skills.extend(
            self.ensure_list(
                data.get("skills")
            )
        )

        # Languages
        skills.extend(
            self.ensure_list(
                data.get("languages")
            )
        )

        # Topics
        skills.extend(
            self.ensure_list(
                data.get("topics")
            )
        )

        profile = {
            "candidate_id": data.get("id"),
            "name": data.get("name")
            or data.get("login"),
            "headline": data.get("bio"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "skills": skills,
            "experience": data.get(
                "experience",
                [],
            ),
            "education": data.get(
                "education",
                [],
            ),
            "location": {
                "city": data.get("city"),
                "region": data.get("region"),
                "country": data.get("country"),
            },
            "links": {
                "github": data.get("html_url"),
                "portfolio": data.get("blog"),
                "linkedin": data.get("linkedin"),
                "other": self.ensure_list(
                    data.get("other_links")
                ),
            },
        }

        return profile