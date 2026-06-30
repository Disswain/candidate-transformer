from src.merge.resolver import MergeResolver
from src.models.candidate import Candidate


def test_merge_duplicate_phone():
    c1 = Candidate(phones=["+14155551234"])
    c2 = Candidate(phones=["+14155551234"])

    merged = MergeResolver().merge([c1, c2])

    assert merged.phones == ["+14155551234"]