from src.normalizers.phone import PhoneNormalizer
from src.models.intermediate import IntermediateCandidate


def test_phone_normalization():
    candidate = IntermediateCandidate(
        source="test",
        phones=["+1 4155551234"]
    )

    result = PhoneNormalizer().normalize(candidate)

    assert result.phones == ["+14155551234"]