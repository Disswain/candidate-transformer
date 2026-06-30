from src.normalizers.name import NameNormalizer
from src.models.intermediate import IntermediateCandidate


def test_name_normalization():
    candidate = IntermediateCandidate(
        source="test",
        full_name="dr. john   anderson"
    )

    result = NameNormalizer().normalize(candidate)

    assert result.full_name == "John Anderson"