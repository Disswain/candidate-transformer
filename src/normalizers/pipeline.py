"""
Normalization Pipeline.

Runs all normalizers and merges their outputs into a single
canonical Candidate object.
"""

from __future__ import annotations

from src.models.candidate import Candidate
from src.models.intermediate import IntermediateCandidate
from src.models.provenance import Provenance

from src.normalizers.name import NameNormalizer
from src.normalizers.email import EmailNormalizer
from src.normalizers.phone import PhoneNormalizer
from src.normalizers.location import LocationNormalizer
from src.normalizers.urls import URLNormalizer
from src.normalizers.dates import DateNormalizer
from src.normalizers.skills import SkillNormalizer


class NormalizationPipeline:
    """
    Executes every normalizer in sequence.
    """

    def __init__(self) -> None:

        self.name = NameNormalizer()

        self.email = EmailNormalizer()

        self.phone = PhoneNormalizer()

        self.location = LocationNormalizer()

        self.urls = URLNormalizer()

        self.dates = DateNormalizer()

        self.skills = SkillNormalizer()

    # ---------------------------------------------------------

    def normalize(
        self,
        candidate: IntermediateCandidate,
    ) -> Candidate:
        """
        Normalize one IntermediateCandidate into one
        canonical Candidate.
        """

        result = Candidate()

        # ----------------------------------------------
        # Name
        # ----------------------------------------------

        self._merge(
            result,
            self.name.normalize(candidate),
        )

        # ----------------------------------------------
        # Email
        # ----------------------------------------------

        self._merge(
            result,
            self.email.normalize(candidate),
        )

        # ----------------------------------------------
        # Phone
        # ----------------------------------------------

        self._merge(
            result,
            self.phone.normalize(candidate),
        )

        # ----------------------------------------------
        # Location
        # ----------------------------------------------

        self._merge(
            result,
            self.location.normalize(candidate),
        )

        # ----------------------------------------------
        # URLs
        # ----------------------------------------------

        self._merge(
            result,
            self.urls.normalize(candidate),
        )

        # ----------------------------------------------
        # Dates
        # ----------------------------------------------

        self._merge(
            result,
            self.dates.normalize(candidate),
        )

        # ----------------------------------------------
        # Skills
        # ----------------------------------------------

        self._merge(
            result,
            self.skills.normalize(candidate),
        )

        # ----------------------------------------------
        # Provenance
        # ----------------------------------------------

        result.provenance.append(
            Provenance(
                field="candidate",
                source=candidate.source,
                method="normalization",
            )
        )
        
        

        return result

    # ---------------------------------------------------------

    @staticmethod
    def _merge(
        target: Candidate,
        source: Candidate,
    ) -> None:
        """
        Merge populated fields from one Candidate into another.
        """

        if source.candidate_id:
            target.candidate_id = source.candidate_id

        if source.full_name:
            target.full_name = source.full_name

        if source.headline:
            target.headline = source.headline

        if source.years_experience is not None:
            target.years_experience = source.years_experience

        if source.emails:
            target.emails = source.emails

        if source.phones:
            target.phones = source.phones

        if (
            source.location.city
            or source.location.region
            or source.location.country
        ):
            target.location = source.location

        if (
            source.links.linkedin
            or source.links.github
            or source.links.portfolio
            or source.links.other
        ):
            target.links = source.links

        if source.skills:
            target.skills = source.skills

        if source.experience:
            target.experience = source.experience

        if source.education:
            target.education = source.education

        if source.provenance:
            target.provenance.extend(source.provenance)

        if source.confidence:
            target.confidence = source.confidence
    