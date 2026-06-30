"""
ATS JSON Extractor.
"""

from __future__ import annotations

from typing import List

from src.models.candidate import Candidate
from src.utils.file_loader import FileLoader
from src.utils.logger import logger
from src.interfaces.extractor import BaseExtractor

class JSONExtractor(BaseExtractor):
    """
    Extract Candidate objects from ATS JSON.
    """

    def extract(self, path: str) -> List[Candidate]:

        logger.info("Loading ATS JSON: %s", path)

        data = FileLoader.load_json(path)

        # Support both a single candidate object
        # and a list of candidates.

        if isinstance(data, dict):
            records = [data]

        elif isinstance(data, list):
            records = data

        else:
            raise ValueError("Unsupported ATS JSON format.")

        candidates: List[Candidate] = []

        for record in records:

            candidate_data = record.get("candidate", record)

            contact = candidate_data.get("contact", {})

            candidate = Candidate(
                full_name=candidate_data.get("name"),
                emails=[contact["email"]]
                if contact.get("email")
                else [],
                phones=[contact["phone"]]
                if contact.get("phone")
                else [],
                headline=candidate_data.get("headline"),
                skills=candidate_data.get("skills", []),
            )

            candidates.append(candidate)

        logger.info(
            "Loaded %d candidates from ATS JSON",
            len(candidates),
        )

        return candidates