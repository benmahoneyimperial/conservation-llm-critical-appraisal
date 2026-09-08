"""Retry transient network failures. Prevents a brief outage wiping out a long run."""

import random
import time

import requests

MAX_ATTEMPTS = 4
BASE_DELAY_SECONDS = 2

RETRYABLE_STATUS = {408, 409, 429, 500, 502, 503, 504}


def is_retryable(exc: Exception) -> bool:
    if isinstance(exc, (requests.ConnectionError, requests.Timeout)):
        return True
    if isinstance(exc, requests.HTTPError) and exc.response is not None:
        return exc.response.status_code in RETRYABLE_STATUS
    return False


def with_retry(call):
    """Call a zero-argument function, retrying transient failures with backoff."""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return call()
        except Exception as exc:  # noqa: BLE001 - re-raised below when not retryable
            if attempt == MAX_ATTEMPTS or not is_retryable(exc):
                raise
            delay = BASE_DELAY_SECONDS * (2 ** (attempt - 1)) + random.uniform(0, 1)
            print(f"  retry {attempt}/{MAX_ATTEMPTS - 1} in {delay:.1f}s ({type(exc).__name__})")
            time.sleep(delay)
    return None
