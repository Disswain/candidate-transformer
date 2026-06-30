"""
Canonical Candidate Models

This module defines the canonical schema shared by the entire pipeline.

Every extractor MUST output these models.
Every normalizer works on these models.
Every merge stage consumes these models.
Every projection stage produces these models.

Author:
    Candidate Transformer

Python:
    3.11+
"""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, HttpUrl
from src.models.skill import Skill

# ----------------------------------------------------------
# Location
# ----------------------------------------------------------


class Location(BaseModel):
    city: Optional[str] = None
    region: Optional[str] = None
    country: Optional[str] = None


# ----------------------------------------------------------
# Links
# ----------------------------------------------------------


class Links(BaseModel):
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None
    portfolio: Optional[HttpUrl] = None
    other: List[HttpUrl] = Field(default_factory=list)


# ----------------------------------------------------------
# Experience
# ----------------------------------------------------------


class Experience(BaseModel):
    company: Optional[str] = None
    title: Optional[str] = None

    start_date: Optional[str] = None
    end_date: Optional[str] = None

    description: Optional[str] = None


# ----------------------------------------------------------
# Education
# ----------------------------------------------------------


class Education(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    field: Optional[str] = None

    start_date: Optional[str] = None
    end_date: Optional[str] = None


# ----------------------------------------------------------
# Provenance
# ----------------------------------------------------------


class Provenance(BaseModel):
    field: str
    source: str
    method: str


# ----------------------------------------------------------
# Confidence
# ----------------------------------------------------------


class Confidence(BaseModel):
    full_name: float = 0.0
    emails: float = 0.0
    phones: float = 0.0
    location: float = 0.0
    skills: float = 0.0
    experience: float = 0.0
    education: float = 0.0
    overall: float = 0.0


# ----------------------------------------------------------
# Candidate
# ----------------------------------------------------------


class Candidate(BaseModel):
    """
    Canonical Candidate Model.

    Entire pipeline works exclusively on this model.
    """

    model_config = ConfigDict(
        validate_assignment=True,
        extra="ignore"
    )

    candidate_id: Optional[str] = None

    full_name: Optional[str] = None

    emails: List[EmailStr] = Field(default_factory=list)

    phones: List[str] = Field(default_factory=list)

    location: Location = Field(default_factory=Location)

    links: Links = Field(default_factory=Links)

    headline: Optional[str] = None

    years_experience: Optional[float] = None

    skills: List[Skill] = Field(default_factory=list)

    experience: List[Experience] = Field(default_factory=list)

    education: List[Education] = Field(default_factory=list)

    provenance: List[Provenance] = Field(default_factory=list)

    confidence: Confidence = Field(default_factory=Confidence)