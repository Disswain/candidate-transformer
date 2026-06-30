"""
Skill Normalizer.

Responsibilities
----------------
- Trim whitespace
- Canonicalize skills
- Remove duplicates
- Stable ordering
"""

from __future__ import annotations

from src.interfaces.normalizer import BaseNormalizer
from src.models.candidate import Candidate
from src.models.intermediate import IntermediateCandidate
from src.models.skill import Skill


class SkillNormalizer(BaseNormalizer):
    """
    Normalize candidate skills.
    """

    SKILL_MAP = {
        # Python
        "python": "Python",
        "python3": "Python",
        "python 3": "Python",

        # JavaScript
        "javascript": "JavaScript",
        "js": "JavaScript",

        # C++
        "cpp": "C++",
        "c++": "C++",

        # React
        "reactjs": "React",
        "react.js": "React",
        "react": "React",

        # Node
        "nodejs": "Node.js",
        "node": "Node.js",
        "node.js": "Node.js",

        # AI
        "ai": "Artificial Intelligence",
        "artificial intelligence": "Artificial Intelligence",

        # ML
        "ml": "Machine Learning",
        "machinelearning": "Machine Learning",
        "machine learning": "Machine Learning",

        # SQL
        "sql": "SQL",

        # Others
        "fastapi": "FastAPI",
        "django": "Django",
        "flask": "Flask",
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "git": "Git",
        "linux": "Linux",
    }

    def normalize(
        self,
        candidate: IntermediateCandidate,
    ) -> Candidate:

        result = Candidate(
            candidate_id=candidate.candidate_id,
            full_name=candidate.full_name,
            headline=candidate.headline,
            years_experience=candidate.years_experience,
            emails=candidate.emails,
            phones=candidate.phones,
        )

        normalized: list[Skill] = []
        seen: set[str] = set()

        for skill in candidate.skills:

            if skill is None:
                continue

            if not isinstance(skill, str):
                skill = str(skill)

            skill = skill.strip()

            if not skill:
                continue

            key = skill.lower()

            canonical = self.SKILL_MAP.get(
                key,
                skill.title(),
            )

            if canonical not in seen:

                seen.add(canonical)

                normalized.append(
                    Skill(
                        name=canonical,
                    )
                )

        normalized.sort(
            key=lambda s: s.name
        )

        result.skills = normalized

        return result