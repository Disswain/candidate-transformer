"""
File Loader Utilities

Provides safe, reusable methods for reading supported input files.

Features
--------
- UTF-8 / UTF-16 encoding detection
- Safe JSON loading
- Safe CSV loading
- Safe TXT loading
- Safe PDF extraction
- Consistent exceptions
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd
import pdfplumber
from charset_normalizer import from_path

from src.utils.logger import get_logger

logger = get_logger(__name__)


class FileLoaderError(Exception):
    """Raised when a file cannot be loaded."""


class FileLoader:
    """
    Utility class for loading supported file formats.
    """

    @staticmethod
    def detect_encoding(path: str | Path) -> str:
        """
        Detect file encoding using charset-normalizer.
        """
        result = from_path(str(path)).best()

        if result is None or result.encoding is None:
            return "utf-8"

        return result.encoding

    @classmethod
    def read_json(cls, path: str | Path) -> dict[str, Any]:
        file = Path(path)

        if not file.exists():
            raise FileLoaderError(f"File not found: {file}")

        encoding = cls.detect_encoding(file)

        try:
            with file.open("r", encoding=encoding) as f:
                return json.load(f)

        except json.JSONDecodeError as exc:
            logger.exception("Invalid JSON: %s", file)
            raise FileLoaderError(f"Invalid JSON: {file}") from exc

    @classmethod
    def read_csv(cls, path: str | Path) -> pd.DataFrame:
        file = Path(path)

        if not file.exists():
            raise FileLoaderError(f"File not found: {file}")

        encoding = cls.detect_encoding(file)

        try:
            return pd.read_csv(file, encoding=encoding)

        except Exception as exc:
            logger.exception("Failed to read CSV: %s", file)
            raise FileLoaderError(f"Invalid CSV: {file}") from exc

    @classmethod
    def read_text(cls, path: str | Path) -> str:
        file = Path(path)

        if not file.exists():
            raise FileLoaderError(f"File not found: {file}")

        encoding = cls.detect_encoding(file)

        try:
            with file.open(
                "r",
                encoding=encoding,
                errors="replace",
            ) as f:
                return f.read()

        except Exception as exc:
            logger.exception("Failed to read text file: %s", file)
            raise FileLoaderError(f"Invalid text file: {file}") from exc

    @classmethod
    def read_pdf(cls, path: str | Path) -> str:
        file = Path(path)

        if not file.exists():
            raise FileLoaderError(f"File not found: {file}")

        try:
            pages: list[str] = []

            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        pages.append(text)

            return "\n".join(pages)

        except Exception as exc:
            logger.exception("Failed to read PDF: %s", file)
            raise FileLoaderError(f"Corrupted PDF: {file}") from exc