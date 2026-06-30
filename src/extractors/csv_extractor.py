"""
Recruiter CSV Extractor.

Reads recruiter CSV files and converts each row into an
IntermediateCandidate.

Responsibilities
----------------
- Read recruiter CSV
- Validate required columns
- Handle missing values
- Ignore unknown columns
- Never normalize data
- Never merge data
"""

from __future__ import annotations

from typing import Any

import pandas as pd

from src.interfaces.extractor import BaseExtractor
from src.models.intermediate import IntermediateCandidate
from src.utils.constants import SOURCE_RECRUITER
from src.utils.file_loader import FileLoader
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CSVExtractor(BaseExtractor):
    """
    Extract candidates from recruiter CSV.
    """

    REQUIRED_COLUMNS = {
        "full_name",
        "email",
        "phone",
    }

    OPTIONAL_COLUMNS = {
        "headline",
        "city",
        "region",
        "country",
        "linkedin",
        "github",
        "portfolio",
        "years_experience",
        "skills",
    }

    def extract(
        self,
        source: str,
    ) -> list[IntermediateCandidate]:

        logger.info("Reading recruiter CSV: %s", source)

        dataframe = FileLoader.read_csv(source)

        self._validate_columns(dataframe)

        candidates: list[IntermediateCandidate] = []

        for index, row in dataframe.iterrows():

            try:

                candidate = self._parse_row(row)

                candidates.append(candidate)

            except Exception as exc:

                logger.exception(
                    "Failed to parse row %d: %s",
                    index,
                    exc,
                )

        logger.info(
            "Successfully extracted %d candidate(s).",
            len(candidates),
        )

        return candidates

    def _validate_columns(
        self,
        dataframe: pd.DataFrame,
    ) -> None:

        columns = {column.strip() for column in dataframe.columns}

        missing = self.REQUIRED_COLUMNS - columns

        if missing:
            raise ValueError(
                f"Missing required columns: {sorted(missing)}"
            )

    def _parse_row(
        self,
        row: pd.Series,
    ) -> IntermediateCandidate:

        def value(name: str) -> Any:
            item = row.get(name)

            if pd.isna(item):
                return None

            if isinstance(item, str):
                item = item.strip()

                if not item:
                    return None

            return item

        skills = []

        raw_skills = value("skills")

        if raw_skills:

            skills = [
                skill.strip()
                for skill in str(raw_skills).split(",")
                if skill.strip()
            ]

        years = value("years_experience")

        if years is not None:
            try:
                years = float(years)
            except (TypeError, ValueError):
                years = None

        return IntermediateCandidate(

            source=SOURCE_RECRUITER,

            full_name=value("full_name"),

            headline=value("headline"),

            years_experience=years,

            emails=[
                value("email")
            ] if value("email") else [],

            phones=[
                str(value("phone"))
            ] if value("phone") else [],

            city=value("city"),

            region=value("region"),

            country=value("country"),

            linkedin=value("linkedin"),

            github=value("github"),

            portfolio=value("portfolio"),

            skills=skills,

            metadata={
                "row_source": "recruiter_csv"
            },
        )