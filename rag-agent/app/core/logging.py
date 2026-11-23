
import logging

from app.core.config import settings


def setup_logging() -> None:
    """
    Configure application-wide logging.
    """

    log_level = getattr(
        logging,
        settings.log_level.upper(),
        logging.INFO,
    )

    logging.basicConfig(
        level=log_level,
        format=(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
    )


def get_logger(name: str) -> logging.Logger:
    """
    Return a named logger.
    """

    return logging.getLogger(name)
