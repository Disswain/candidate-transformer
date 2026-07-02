"""
Resume Text Extractor.

Parses a plain text resume (.txt) and converts it into an
IntermediateCandidate.

Responsibilities:
- Read resume text
- Extract basic candidate information
- Preserve raw data
- Never normalize
- Never merge
"""

from __future__ import annotations
import re
import phonenumbers
from src.extractors.base_profile_parser import BaseProfileParser
from src.models.intermediate import IntermediateCandidate
from src.utils.constants import SOURCE_RESUME_TXT
from src.utils.file_loader import FileLoader
from src.utils.logger import get_logger

logger = get_logger(__name__)


class ResumeParser(BaseProfileParser):
    """
    Resume TXT parser.
    """

    EMAIL_PATTERN = re.compile(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    )

    # Improved phone regex
    PHONE_PATTERN = re.compile(
        r"\+?\d[\d\s().-]{8,}\d"
    )

    LINKEDIN_PATTERN = re.compile(
        r"https?://(?:www\.)?linkedin\.com/[^\s]+",
        re.IGNORECASE,
    )

    GITHUB_PATTERN = re.compile(
        r"https?://(?:www\.)?github\.com/[^\s]+",
        re.IGNORECASE,
    )

    URL_PATTERN = re.compile(
        r"https?://[^\s]+",
        re.IGNORECASE,
    )

    def extract(
        self,
        source: str,
    ) -> list[IntermediateCandidate]:

        logger.info("Reading resume: %s", source)

        text = FileLoader.read_text(source)

        profile = self._parse_resume(text)

        candidate = self.build_candidate(
            source=SOURCE_RESUME_TXT,
            data=profile,
            metadata={
                "source_file": source,
                "parser": "resume_txt",
            },
        )

        logger.info("Resume parsed successfully.")

        return [candidate]

    def _parse_resume(
        self,
        text: str,
    ) -> dict:

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        name = lines[0] if lines else None

        email = None
        phone = None
        linkedin = None
        github = None

        skills = []

        emails = self.EMAIL_PATTERN.findall(text)
        if emails:
            email = emails[0].strip()

        phones = self.PHONE_PATTERN.findall(text)

        if phones:

            raw_phone = phones[0].strip()

            try:

                parsed = phonenumbers.parse(
                    raw_phone,
                    None,
                )

                if phonenumbers.is_valid_number(parsed):

                    phone = phonenumbers.format_number(
                        parsed,
                        phonenumbers.PhoneNumberFormat.E164,
                    )

                else:

                    phone = raw_phone

            except phonenumbers.NumberParseException:

                phone = raw_phone

        linkedin_urls = self.LINKEDIN_PATTERN.findall(text)
        if linkedin_urls:
            linkedin = linkedin_urls[0]

        github_urls = self.GITHUB_PATTERN.findall(text)
        if github_urls:
            github = github_urls[0]

        all_urls = self.URL_PATTERN.findall(text)

        skills_section = False

        for line in lines:

            lower = line.lower()

            if "skills" in lower:
                skills_section = True
                continue

            if skills_section:

                if lower.startswith(
                    (
                        "education",
                        "experience",
                        "projects",
                        "certifications",
                        "summary",
                    )
                ):
                    break

                for skill in line.split(","):

                    skill = skill.strip()

                    if skill:
                        skills.append(skill)

        other_links = [
            url
            for url in all_urls
            if url not in {
                linkedin,
                github,
            }
        ]

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "skills": skills,
            "experience": [],
            "education": [],
            "location": {},
            "links": {
                "linkedin": linkedin,
                "github": github,
                "portfolio": None,
                "other": other_links,
            },
        }