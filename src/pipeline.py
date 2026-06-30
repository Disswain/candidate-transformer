"""
Candidate Transformation Pipeline.
"""

from __future__ import annotations

import json
from pathlib import Path

from src.extractors.csv_extractor import CSVExtractor
from src.extractors.github_parser import GitHubParser
from src.extractors.json_extractor import JSONExtractor
from src.extractors.linkedin_parser import LinkedInParser
from src.extractors.pdf_parser import PDFParser
from src.extractors.registry import ExtractorRegistry
from src.extractors.resume_parser import ResumeParser

from src.merge.confidence import ConfidenceCalculator
from src.merge.resolver import MergeResolver

from src.normalizers.pipeline import NormalizationPipeline

from src.projection.projector import CandidateProjector

from src.validation.validator import CandidateValidator

from src.utils.config import ConfigService
from src.utils.logger import get_logger

logger = get_logger(__name__)


class CandidatePipeline:
    """
    Complete ETL Pipeline.
    """

    def __init__(
        self,
        config_path: str,
    ) -> None:

        self.config_service = ConfigService(
            config_path
        )

        self.registry = ExtractorRegistry()

        self._register_extractors()

        self.normalizer = NormalizationPipeline()

        self.merger = MergeResolver()

        self.confidence = ConfidenceCalculator()

        self.validator = CandidateValidator()

        self.projector = CandidateProjector(
            self.config_service.config.model_dump()
        )

    # ---------------------------------------------------------

    def _register_extractors(self) -> None:

        self.registry.register(
            ".csv",
            CSVExtractor(),
        )

        self.registry.register(
            ".json",
            JSONExtractor(),
        )

        self.registry.register(
            ".txt",
            ResumeParser(),
        )

        self.registry.register(
            ".pdf",
            PDFParser(),
        )

        self.registry.register(
            "linkedin",
            LinkedInParser(),
        )

        self.registry.register(
            "github",
            GitHubParser(),
        )

    # ---------------------------------------------------------

    def run(
        self,
        input_directory: str,
        output_file: str,
    ) -> None:

        logger.info("Pipeline started.")

        normalized_candidates = []

        for file in sorted(
            Path(input_directory).rglob("*")
        ):

            if not file.is_file():
                continue

            try:

                extractor = self.registry.get(
                    str(file)
                )

            except Exception:

                continue

            logger.info(
                "Processing %s",
                file.name,
            )

            raw_candidates = extractor.extract(
                str(file)
            )

            for raw in raw_candidates:

                candidate = self.normalizer.normalize(
                    raw
                )

                normalized_candidates.append(
                    candidate
                )

        merged = self.merger.merge(
            normalized_candidates
        )
        # print("\n--- BEFORE MERGE ---")
        # for i, c in enumerate(normalized_candidates):
        #     print(i, c.phones)

        #     print("\n--- AFTER MERGE ---")
        #     print(merged.phones)
        # print("\n===== AFTER MERGE =====")
        # print(merged.phones)
        # print(len(merged.phones))


        merged.confidence = self.confidence.calculate(
            merged
        )

        validation = self.validator.validate(
            merged
        )

        if not validation.valid:

            raise ValueError(
                validation.errors
            )

        output = self.projector.project(
            merged
        )

        # print("\n===== AFTER PROJECTOR =====")
        # print(output["phones"])
        # print(len(output["phones"]))

        Path(output_file).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as f:

            json.dump(
                output,
                f,
                indent=4,
                ensure_ascii=False,
            )

        logger.info(
            "Output written to %s",
            output_file,
        )