# SPDX-License-Identifier: Apache-2.0

import sys

from loguru import logger


def configure_logging(debug: bool = False) -> None:
    """Configure logging based on debug flag."""
    logger.remove()  # Remove default handler

    if debug:
        level = "DEBUG"
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        )
    else:
        level = "INFO"
        log_format = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<level>{message}</level>"
        )

    logger.add(sys.stderr, format=log_format, level=level, colorize=True)
