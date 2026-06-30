"""
Skill Mapper.

Converts raw skill representations into a normalized
list for the IntermediateCandidate.

NOTE:
No canonicalization happens here.
That belongs in SkillNormalizer.
"""

from __future__ import annotations

from typing import Any


class SkillMapper:
    """
    Maps arbitrary skill formats into a list[str].
    """

    @staticmethod
    def from_value(value: Any) -> list[str]:
        """
        Supported inputs

        "Python"

        ["Python","Java"]

        [{"name":"Python"},{"name":"Java"}]
        """

        if value is None:
            return []

        if isinstance(value, str):
            return [value.strip()] if value.strip() else []

        if not isinstance(value, list):
            return []

        skills: list[str] = []

        for item in value:

            if isinstance(item, str):

                item = item.strip()

                if item:
                    skills.append(item)

            elif isinstance(item, dict):

                name = item.get("name")

                if isinstance(name, str):

                    name = name.strip()

                    if name:
                        skills.append(name)

        return skills