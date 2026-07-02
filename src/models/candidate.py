"""
Canonical Candidate Model

This model represents the normalized candidate profile used
throughout the remainder of the pipeline.

Pipeline given below:

IntermediateCandidate
        │
        ▼
Normalization
        │
        ▼
Candidate
        │
        ▼
Validation
        ▼
Merge
        ▼
Projection
        ▼
Output JSON
"""

from __future__ import annotations
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from src.models.confidence import Confidence
from src.models.education import Education
from src.models.experience import Experience
from src.models.links import Links
from src.models.location import Location
from src.models.provenance import Provenance
from src.models.skill import Skill


class Candidate(BaseModel):
    """
    Canonical Candidate Profile.
    """

    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True,
    )

    # Identity-
  

    candidate_id: str | None = None

    full_name: str | None = None

    headline: str | None = None

    years_experience: float | None = None

    # Contact-

    emails: list[EmailStr] = Field(default_factory=list)

    phones: list[str] = Field(default_factory=list)

    # Location-

    location: Location = Field(
        default_factory=Location
    )

    # Links-
    links: Links = Field(
        default_factory=Links
    )

    # Skills-

    skills: list[Skill] = Field(
        default_factory=list
    )

    # Experience-

    experience: list[Experience] = Field(
        default_factory=list
    )

    # Education-

    education: list[Education] = Field(
        default_factory=list
    )

    # Provenance-

    provenance: list[Provenance] = Field(
        default_factory=list
    )

    # Confidence-

    confidence: Confidence = Field(
        default_factory=Confidence
    )