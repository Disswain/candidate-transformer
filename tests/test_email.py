from src.normalizers.email import EmailNormalizer
from src.models.intermediate import IntermediateCandidate


def test_email_normalization():
    candidate = IntermediateCandidate(
        source="test",
        emails=[" John.Anderson@Example.com "]
    )

    result = EmailNormalizer().normalize(candidate)

    assert str(result.emails[0]) == "john.anderson@example.com"