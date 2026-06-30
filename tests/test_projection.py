from src.projection.projector import CandidateProjector
from src.models.candidate import Candidate


def test_projection():
    config = {
        "fields": [
            {"path": "full_name"},
            {"path": "emails"},
        ],
        "projection": {
            "include_confidence": False,
            "include_provenance": False,
            "on_missing": "null",
        },
    }

    candidate = Candidate(
        full_name="John Anderson",
        emails=["john@example.com"],
    )

    result = CandidateProjector(config).project(candidate)

    assert result["full_name"] == "John Anderson"
    assert result["emails"] == ["john@example.com"]