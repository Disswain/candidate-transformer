"""
Education Mapper.

Ensures education is always returned as
list[dict[str, Any]].
"""

from __future__ import annotations
from typing import Any


class EducationMapper:

    @staticmethod
    def from_value(
        value: Any,
    ) -> list[dict[str, Any]]:

        if value is None:
            return []

        if not isinstance(value, list):
            return []

        education: list[dict[str, Any]] = []

        for item in value:

            if isinstance(item, dict):
                education.append(item)

        return education