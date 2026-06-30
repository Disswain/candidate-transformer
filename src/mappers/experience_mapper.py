"""
Experience Mapper.

Ensures experience is always returned as
list[dict[str, Any]].
"""

from __future__ import annotations

from typing import Any


class ExperienceMapper:

    @staticmethod
    def from_value(
        value: Any,
    ) -> list[dict[str, Any]]:

        if value is None:
            return []

        if not isinstance(value, list):
            return []

        experience: list[dict[str, Any]] = []

        for item in value:

            if isinstance(item, dict):
                experience.append(item)

        return experience