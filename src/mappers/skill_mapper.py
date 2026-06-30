"""
Maps raw skill data into Skill models.
"""

from __future__ import annotations

from src.models.skill import Skill


class SkillMapper:

    @staticmethod
    def from_list(skills: list) -> list[Skill]:
        """
        Accepts:
        [
            "Python",
            {"name": "Java"},
            "React"
        ]

        Returns:
        List[Skill]
        """

        result: list[Skill] = []

        for skill in skills:

            if isinstance(skill, str):

                skill = skill.strip()

                if skill:
                    result.append(
                        Skill(name=skill)
                    )

            elif isinstance(skill, dict):

                name = skill.get("name", "").strip()

                if name:
                    result.append(
                        Skill(name=name)
                    )

        return result