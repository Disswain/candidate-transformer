from pathlib import Path

from src.pipeline import CandidatePipeline


def test_pipeline_runs():
    pipeline = CandidatePipeline("config/default.json")

    output = "outputs/test_result.json"

    pipeline.run("sample_data", output)

    assert Path(output).exists()