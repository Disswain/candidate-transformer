"""
Application-wide constants.
"""

from __future__ import annotations

# ---------------------------------------------------------
# Supported Sources
# ---------------------------------------------------------

SOURCE_RECRUITER = "recruiter_csv"

SOURCE_ATS = "ats_json"

SOURCE_LINKEDIN = "linkedin"

SOURCE_GITHUB = "github"

SOURCE_RESUME_TXT = "resume_txt"

SOURCE_RESUME_PDF = "resume_pdf"

# ---------------------------------------------------------
# Source Priority
# Higher index = lower priority
# ---------------------------------------------------------

SOURCE_PRIORITY = (
    SOURCE_RECRUITER,
    SOURCE_ATS,
    SOURCE_LINKEDIN,
    SOURCE_GITHUB,
    SOURCE_RESUME_PDF,
    SOURCE_RESUME_TXT,
)

# ---------------------------------------------------------
# Supported Countries
# ---------------------------------------------------------

DEFAULT_COUNTRY = "IN"

# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

LOGGER_NAME = "candidate-transformer"

# ---------------------------------------------------------
# Date Formats
# ---------------------------------------------------------

SUPPORTED_DATE_FORMATS = (
    "%Y-%m",
    "%Y",
    "%b %Y",
    "%B %Y",
    "%m/%Y",
)

# ---------------------------------------------------------
# Common Name Prefixes
# ---------------------------------------------------------

NAME_PREFIXES = {
    "mr",
    "mrs",
    "ms",
    "dr",
    "prof",
}

# ---------------------------------------------------------
# Empty Values
# ---------------------------------------------------------

EMPTY_VALUES = {
    "",
    "na",
    "n/a",
    "none",
    "null",
    "-",
}