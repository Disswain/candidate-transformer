"""
Extractor Registry.

Maps file names and extensions to the appropriate extractor.

The pipeline never instantiates extractors directly.
"""

from __future__ import annotations

from pathlib import Path

from src.interfaces.extractor import BaseExtractor


class ExtractorRegistry:
    """
    Registry for all available extractors.
    """

    def __init__(self) -> None:
        self._registry: dict[str, BaseExtractor] = {}

    def register(
        self,
        key: str,
        extractor: BaseExtractor,
    ) -> None:
        """
        Register an extractor.

        Example
        -------
        registry.register(".csv", CSVExtractor())
        """
        self._registry[key.lower()] = extractor

    def get(
        self,
        source: str,
    ) -> BaseExtractor:
        """
        Resolve an extractor from a file path.
        """

        filename = Path(source).name.lower()

        # Special cases first
        if filename == "linkedin.json":
            return self._registry["linkedin"]

        if filename == "github.json":
            return self._registry["github"]

        suffix = Path(source).suffix.lower()

        if suffix in self._registry:
            return self._registry[suffix]

        raise ValueError(
            f"No extractor registered for '{source}'."
        )

    @property
    def registered(self) -> tuple[str, ...]:
        """
        Return all registered extractor keys.
        """
        return tuple(sorted(self._registry.keys()))