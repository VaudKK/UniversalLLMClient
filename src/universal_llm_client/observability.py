import logging

import structlog


def configure_logging():
    logging.basicConfig(
        format = "%(message)s",
        level = logging.INFO
    )

    structlog.configure(
        processors = [
            structlog.processors.TimeStamper(fmt = "iso"),
            structlog.processors.JSONRenderer(),
            structlog.processors.add_log_level,
        ],
        logger_factory = structlog.stdlib.LoggerFactory(),
    )

logger = structlog.get_logger()