"""
Recruiter CSV Extractor

Converts recruiter CSV into Candidate objects.

Each row = one candidate.
"""

from __future__ import annotations

from typing import List

from src.models.candidate import Candidate
from src.utils.file_loader import FileLoader
from src.utils.logger import logger
from src.interfaces.extractor import BaseExtractor

class CSVExtractor(BaseExtractor):
    """
    Extract Candidate objects from recruiter CSV.
    """

    def extract(self, path: str) -> List[Candidate]:
        logger.info("Loading recruiter CSV: %s", path)

        df = FileLoader.load_csv(path)

        candidates: List[Candidate] = []

        for _, row in df.iterrows():

            candidate = Candidate(
                full_name=row.get("full_name"),
                emails=[row["email"]]
                if row.get("email")
                else [],
                phones=[str(row["phone"])]
                if row.get("phone")
                else [],
                headline=row.get("headline"),
                skills=[],
            )

            candidates.append(candidate)

        logger.info(
            "Loaded %d candidates from recruiter CSV",
            len(candidates),
        )

        return candidates