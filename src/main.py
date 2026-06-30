"""
Application Entry Point.

Example
-------

python main.py \
    --input sample_data \
    --config config/default.json \
    --output outputs/result.json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from src.pipeline import CandidatePipeline
from src.utils.logger import get_logger

logger = get_logger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """
    Build the CLI argument parser.
    """

    parser = argparse.ArgumentParser(
        prog="candidate-transformer",
        description="Multi-Source Candidate Data Transformer",
    )

    parser.add_argument(
        "--input",
        required=True,
        type=str,
        help="Input directory containing candidate files.",
    )

    parser.add_argument(
        "--config",
        required=True,
        type=str,
        help="Path to configuration JSON.",
    )

    parser.add_argument(
        "--output",
        required=True,
        type=str,
        help="Output JSON file.",
    )

    return parser


def validate_paths(
    input_path: str,
    config_path: str,
) -> None:
    """
    Validate input paths before running.
    """

    if not Path(input_path).exists():
        raise FileNotFoundError(
            f"Input path not found: {input_path}"
        )

    if not Path(config_path).exists():
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}"
        )


def main() -> int:
    """
    CLI entry point.
    """

    parser = build_parser()

    args = parser.parse_args()

    try:

        validate_paths(
            args.input,
            args.config,
        )

        logger.info("Starting Candidate Transformer...")

        pipeline = CandidatePipeline(
            config_path=args.config,
        )

        pipeline.run(
            input_directory=args.input,
            output_file=args.output,
        )

        logger.info("Transformation completed successfully.")

        return 0

    except KeyboardInterrupt:

        logger.warning("Operation cancelled by user.")

        return 130

    except Exception as exc:

        logger.exception("Pipeline failed: %s", exc)

        return 1


if __name__ == "__main__":
    sys.exit(main())