from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class IntermediateCandidate:
    """
    Raw extracted candidate.

    No validation.
    No normalization.
    No confidence.

    Represents exactly what an extractor found.
    """

    source: str

    full_name: str | None = None

    emails: list[str] = field(default_factory=list)

    phones: list[str] = field(default_factory=list)

    city: str | None = None

    region: str | None = None

    country: str | None = None

    linkedin: str | None = None

    github: str | None = None

    portfolio: str | None = None

    other_links: list[str] = field(default_factory=list)

    headline: str | None = None

    skills: list = field(default_factory=list)

    experience: list = field(default_factory=list)

    education: list = field(default_factory=list)