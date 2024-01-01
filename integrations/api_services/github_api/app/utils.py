from fastapi.responses import JSONResponse
import logging
import os

logger = logging.getLogger(__name__)


def load_environment_variables():
    tokens = os.getenv('TOKENS')
    if not tokens:
        logger.error("TOKENS environment variable not set")
        raise ValueError("Missing environment variable: TOKENS")
    concurrency = int(os.getenv('CONCURRENCY') or len(tokens.split(',')))
    return tokens.split(','), concurrency


def handle_exception(request, exc):
    logger.error(f"Unhandled exception occurred: {exc} - Request: {request.url}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )
