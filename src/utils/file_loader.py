"""
Safe file loading utilities.

Supports

- JSON
- CSV
- TXT
- PDF

Handles

- Missing files
- UTF8 / UTF16
- Invalid JSON
- Corrupted PDFs

Never crashes.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pdfplumber

from charset_normalizer import from_path
from src.utils.logger import logger



class FileLoaderError(Exception):
    """Raised when a file cannot be loaded."""


class FileLoader:

    @staticmethod
    def detect_encoding(path: str) -> str:
        result = from_path(path).best()

        if result is None:
            return "utf-8"

        return result.encoding

    @staticmethod
    def load_json(path: str) -> dict:

        file = Path(path)

        if not file.exists():
            raise FileLoaderError(f"Missing file: {path}")

        encoding = FileLoader.detect_encoding(path)

        try:
            with open(file, encoding=encoding) as f:
                return json.load(f)

        except Exception as exc:
            logger.error(exc)
            raise FileLoaderError(path)

    @staticmethod
    def load_csv(path: str) -> pd.DataFrame:

        file = Path(path)

        if not file.exists():
            raise FileLoaderError(path)

        encoding = FileLoader.detect_encoding(path)

        return pd.read_csv(
            file,
            encoding=encoding,
        )

    @staticmethod
    def load_text(path: str) -> str:

        file = Path(path)

        if not file.exists():
            raise FileLoaderError(path)

        encoding = FileLoader.detect_encoding(path)

        with open(
            file,
            encoding=encoding,
            errors="replace",
        ) as f:

            return f.read()

    @staticmethod
    def load_pdf(path: str) -> str:

        file = Path(path)

        if not file.exists():
            raise FileLoaderError(path)

        text = []

        try:

            with pdfplumber.open(file) as pdf:

                for page in pdf.pages:

                    extracted = page.extract_text()

                    if extracted:
                        text.append(extracted)

            return "\n".join(text)

        except Exception as exc:

            logger.error(exc)

            raise FileLoaderError(
                f"Unable to parse PDF: {path}"
            )