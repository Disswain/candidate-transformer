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
        # -----------------------------
        # Programming Languages
        # -----------------------------
        "python": "Python",
        "python3": "Python",
        "python 3": "Python",

        "java": "Java",

        "c": "C",
        "cpp": "C++",
        "c++": "C++",

        "go": "Go",
        "golang": "Go",

        "javascript": "JavaScript",
        "js": "JavaScript",

        "typescript": "TypeScript",
        "ts": "TypeScript",

        # -----------------------------
        # Frameworks
        # -----------------------------
        "react": "React",
        "reactjs": "React",
        "react.js": "React",

        "node": "Node.js",
        "nodejs": "Node.js",
        "node.js": "Node.js",

        "django": "Django",
        "flask": "Flask",
        "fastapi": "FastAPI",

        # -----------------------------
        # Databases
        # -----------------------------
        "sql": "SQL",
        "mysql": "MySQL",
        "postgres": "PostgreSQL",
        "postgresql": "PostgreSQL",
        "mongodb": "MongoDB",

        # -----------------------------
        # Cloud
        # -----------------------------
        "aws": "AWS",
        "amazon web services": "AWS",
        "azure": "Azure",
        "gcp": "Google Cloud",
        "google cloud": "Google Cloud",

        # -----------------------------
        # DevOps
        # -----------------------------
        "docker": "Docker",
        "kubernetes": "Kubernetes",
        "git": "Git",
        "github": "GitHub",
        "linux": "Linux",

        # -----------------------------
        # APIs
        # -----------------------------
        "rest": "REST",
        "rest api": "REST API",
        "restapi": "REST API",
        "graphql": "GraphQL",

        # -----------------------------
        # AI / ML
        # -----------------------------
        "ai": "Artificial Intelligence",
        "artificial intelligence": "Artificial Intelligence",
        "ml": "Machine Learning",
        "machine learning": "Machine Learning",
        "machinelearning": "Machine Learning",
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
            # emails=candidate.emails,
            # phones=candidate.phones,
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

            if canonical.lower() not in seen:

                seen.add(canonical.lower())

                normalized.append(
                    Skill(
                        name=canonical,
                    )
                )

        normalized.sort(
            key=lambda s: s.name.lower(),
        )

        result.skills = normalized

        return result