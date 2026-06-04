"""
Stellar System V2 — Logging Setup
Configures the root logger to write to both console and a rotating file handler.
"""

import logging
import os
from logging.handlers import RotatingFileHandler


def setup_logger(name: str = "stellar") -> logging.Logger:
    """
    Create and configure a logger that writes to stdout and logs/bot.log.

    Args:
        name: Logger name (defaults to 'stellar').

    Returns:
        Configured Logger instance.
    """
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)-8s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # --- Console handler (INFO and above) ---
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # --- File handler (DEBUG and above, rotating 5 MB × 3 backups) ---
    file_handler = RotatingFileHandler(
        filename="logs/bot.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Singleton used across the project
log = setup_logger("stellar")
