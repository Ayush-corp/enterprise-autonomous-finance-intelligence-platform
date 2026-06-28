from app.core.logging import configure_logging
from app.core import get_logger

configure_logging()

logger = get_logger("startup")

logger.info(
    "Application Started",
    version="2.0",
    env="development",
)

logger.info(
    "Fetching Market Data",
    stock="RELIANCE.NS",
)

logger.warning(
    "Retrying Request",
    retry=1,
)

try:
    1 / 0
except Exception:
    logger.exception("Division Error")