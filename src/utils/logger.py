"""
Central logging configuration.

Every module imports logger from here.

Example:
    from utils.logger import logger

    logger.info("Pipeline started")
"""

from __future__ import annotations

import logging
import sys


LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(
    name: str = "candidate-transformer",
    level: int = logging.INFO,
) -> logging.Logger:
    """
    Configure and return a logger.

    Duplicate handlers are avoided so importing this
    module multiple times is safe.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    logger.propagate = False

    return logger


logger = setup_logger()