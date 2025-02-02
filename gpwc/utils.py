import logging
from typing import Any
import uuid

from jsonpath_ng import parse
import requests
from requests.adapters import HTTPAdapter, Retry


def generate_id() -> str:
    return uuid.uuid4().hex


def jpath(data: list | dict, expr: str, default: Any = None) -> Any:
    matches = parse(expr).find(data)
    return matches[0].value if matches else default


def get_nested(data: list | dict, *indices: tuple[int], default: bool = None):
    """
    Safely get a nested value from lists or dictionaries using a sequence of
    indices/keys without throwing errors for missing paths.
    """
    current = data
    for idx in indices:
        if current is None:
            return default
        try:
            current = current[idx]
        except (IndexError, KeyError, TypeError):
            return default
    return current


def new_session_with_retries() -> requests.Session:
    """Create a new request session with retry mechanism"""
    # https://stackoverflow.com/questions/23267409/how-to-implement-retry-mechanism-into-python-requests-library
    headers = {
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8",
    }
    s = requests.Session()
    s.headers.update(headers)
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    adapter = HTTPAdapter(max_retries=retries)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    return s


def create_logger(log_level: str) -> logging.Logger:
    """Create main logger"""
    logging.basicConfig(
        level=log_level,
        format="%(message)s",
        datefmt="%H:%M:%S",
    )
    return logging.getLogger("main")
