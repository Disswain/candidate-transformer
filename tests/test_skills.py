from src.normalizers.skills import SkillNormalizer
from src.models.intermediate import IntermediateCandidate


def test_skill_normalization():
    candidate = IntermediateCandidate(
        source="test",
        skills=["python", "Python", "aws"]
    )

    result = SkillNormalizer().normalize(candidate)

    names = [skill.name for skill in result.skills]

    assert "Python" in names
    assert "AWS" in names
    assert len(names) == 2