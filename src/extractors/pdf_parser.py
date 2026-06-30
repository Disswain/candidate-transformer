"""
PDF Resume Extractor.

Extracts text from a PDF resume and converts it into an
IntermediateCandidate.

The actual parsing logic is reused from ResumeParser.
"""

from __future__ import annotations

from src.extractors.resume_parser import ResumeParser
from src.models.intermediate import IntermediateCandidate
from src.utils.constants import SOURCE_RESUME_PDF
from src.utils.file_loader import FileLoader
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PDFParser(ResumeParser):
    """
    Resume PDF parser.

    Inherits ResumeParser so the parsing logic is not duplicated.
    """

    def extract(
        self,
        source: str,
    ) -> list[IntermediateCandidate]:

        logger.info("Reading PDF resume: %s", source)

        text = FileLoader.read_pdf(source)

        profile = self._parse_resume(text)

        candidate = self.build_candidate(
            source=SOURCE_RESUME_PDF,
            data=profile,
            metadata={
                "source_file": source,
                "parser": "resume_pdf",
            },
        )

        logger.info("PDF resume parsed successfully.")

        return [candidate]