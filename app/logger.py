import logging
import sys


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("semantic_cache")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        "%(levelname)s | %(asctime)s | %(message)s"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


logger = setup_logger()