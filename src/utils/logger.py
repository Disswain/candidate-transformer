"""
Centralized logging configuration.

Every module should import the logger from here.

Example:
    from src.utils.logger import get_logger

    logger = get_logger(__name__)
    logger.info("Pipeline started")
"""

from __future__ import annotations

import logging
import sys
from pathlib import Path


LOG_FORMAT = (
    "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
)

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

DEFAULT_LOG_LEVEL = logging.INFO

_LOGGERS: dict[str, logging.Logger] = {}


def get_logger(
    name: str,
    *,
    level: int = DEFAULT_LOG_LEVEL,
    log_file: str | None = None,
) -> logging.Logger:
    """
    Return a configured logger.

    The logger is configured only once, even if requested
    multiple times.

    Parameters
    ----------
    name:
        Logger name (normally __name__)

    level:
        Logging level

    log_file:
        Optional log file path

    Returns
    -------
    logging.Logger
    """

    if name in _LOGGERS:
        return _LOGGERS[name]

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    formatter = logging.Formatter(
        fmt=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Optional file handler
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(
            log_path,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    _LOGGERS[name] = logger

    return logger