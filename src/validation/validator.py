"""
Candidate Validator.

Validates the canonical Candidate before projection.
"""

from __future__ import annotations

from datetime import datetime

import phonenumbers
import pycountry
from pydantic import EmailStr, TypeAdapter, ValidationError

from src.models.candidate import Candidate
from src.validation.schema import ValidationResult


class CandidateValidator:
    """
    Validates canonical Candidate objects.
    """

    def __init__(self) -> None:
        self.email_adapter = TypeAdapter(EmailStr)

    # -----------------------------------------------------

    def validate(
        self,
        candidate: Candidate,
    ) -> ValidationResult:

        result = ValidationResult()

        self._validate_required(candidate, result)
        self._validate_emails(candidate, result)
        self._validate_phones(candidate, result)
        self._validate_country(candidate, result)
        self._validate_experience(candidate, result)
        self._validate_education(candidate, result)

        result.valid = len(result.errors) == 0

        return result

    # -----------------------------------------------------

    @staticmethod
    def _validate_required(
        candidate: Candidate,
        result: ValidationResult,
    ) -> None:

        if not candidate.full_name:
            result.errors.append(
                "Missing required field: full_name"
            )

    # -----------------------------------------------------

    def _validate_emails(
        self,
        candidate: Candidate,
        result: ValidationResult,
    ) -> None:

        valid_emails = []

        for email in candidate.emails:

            try:

                validated = self.email_adapter.validate_python(
                    str(email)
                )

                valid_emails.append(validated)

            except ValidationError:

                result.warnings.append(
                    f"Invalid email ignored: {email}"
                )

        candidate.emails = valid_emails

    # -----------------------------------------------------

    @staticmethod
    def _validate_phones(
        candidate: Candidate,
        result: ValidationResult,
    ) -> None:

        valid_phones = []

        for phone in candidate.phones:

            try:

                parsed = phonenumbers.parse(
                    phone,
                    None,
                )

                if phonenumbers.is_valid_number(parsed):

                    valid_phones.append(
                        phonenumbers.format_number(
                            parsed,
                            phonenumbers.PhoneNumberFormat.E164,
                        )
                    )

                else:

                    result.warnings.append(
                        f"Invalid phone ignored: {phone}"
                    )

            except phonenumbers.NumberParseException:

                result.warnings.append(
                    f"Invalid phone ignored: {phone}"
                )

        candidate.phones = valid_phones

    # -----------------------------------------------------

    @staticmethod
    def _validate_country(
        candidate: Candidate,
        result: ValidationResult,
    ) -> None:

        country = candidate.location.country

        if country is None:
            return

        try:

            pycountry.countries.lookup(country)

        except LookupError:

            result.warnings.append(
                f"Unknown country: {country}"
            )

            candidate.location.country = None

    # -----------------------------------------------------

    @staticmethod
    def _validate_experience(
        candidate: Candidate,
        result: ValidationResult,
    ) -> None:

        now = datetime.now().strftime("%Y-%m")

        for exp in candidate.experience:

            if (
                exp.start_date
                and exp.start_date > now
            ):

                result.warnings.append(
                    f"Future experience start date: {exp.start_date}"
                )

            if (
                exp.start_date
                and exp.end_date
                and exp.end_date < exp.start_date
            ):

                result.warnings.append(
                    f"Experience end date before start date: {exp.company}"
                )

    # -----------------------------------------------------

    @staticmethod
    def _validate_education(
        candidate: Candidate,
        result: ValidationResult,
    ) -> None:

        now = datetime.now().strftime("%Y-%m")

        for edu in candidate.education:

            if (
                edu.start_date
                and edu.start_date > now
            ):

                result.warnings.append(
                    f"Future education start date: {edu.start_date}"
                )

            if (
                edu.start_date
                and edu.end_date
                and edu.end_date < edu.start_date
            ):

                result.warnings.append(
                    f"Education end date before start date: {edu.institution}"
                )