"""
Intermediate Candidate Model

This model represents raw candidate information extracted from any source.

Every extractor (CSV, ATS, Resume, GitHub, LinkedIn, etc.)
returns IntermediateCandidate objects.

No normalization.
No validation.
No confidence.
No provenance.

Normalization happens later in the pipeline.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class IntermediateCandidate:
    """
    Internal representation before normalization.
    """

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    source: str

    # --------------------------------------------------
    # Identity
    # --------------------------------------------------

    candidate_id: str | None = None

    full_name: str | None = None

    headline: str | None = None

    years_experience: float | None = None

    # --------------------------------------------------
    # Contact
    # --------------------------------------------------

    emails: list[str] = field(default_factory=list)

    phones: list[str] = field(default_factory=list)

    # --------------------------------------------------
    # Location
    # --------------------------------------------------

    city: str | None = None

    region: str | None = None

    country: str | None = None

    # --------------------------------------------------
    # Links
    # --------------------------------------------------

    linkedin: str | None = None

    github: str | None = None

    portfolio: str | None = None

    other_links: list[str] = field(default_factory=list)

    # --------------------------------------------------
    # Raw Skills
    # --------------------------------------------------

    skills: list[Any] = field(default_factory=list)

    # --------------------------------------------------
    # Raw Experience
    # --------------------------------------------------

    experience: list[dict] = field(default_factory=list)

    # --------------------------------------------------
    # Raw Education
    # --------------------------------------------------

    education: list[dict] = field(default_factory=list)

    # --------------------------------------------------
    # Extra Fields
    # --------------------------------------------------

    metadata: dict[str, Any] = field(default_factory=dict)