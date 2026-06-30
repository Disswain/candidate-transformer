from src.normalizers.dates import DateNormalizer
from src.models.intermediate import IntermediateCandidate


def test_date_normalization():
    candidate = IntermediateCandidate(
        source="test",
        experience=[
            {
                "company": "ABC",
                "title": "Dev",
                "start_date": "Jan 2020",
                "end_date": "Dec 2021",
            }
        ]
    )

    result = DateNormalizer().normalize(candidate)

    assert result.experience[0].start_date == "2020-01"
    assert result.experience[0].end_date == "2021-12"