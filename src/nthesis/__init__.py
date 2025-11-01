"""Python client library for the nthesis API."""

from .nthesis import (
    BadRequestError,
    ConflictError,
    NotFoundError,
    Nthesis,
    NthesisError,
    UnauthorizedError,
    UnexpectedResponseError,
)
from .models import NewItemResponse, Store

__all__ = [
    "Nthesis",
    "NthesisError",
    "UnauthorizedError",
    "ConflictError",
    "BadRequestError",
    "NotFoundError",
    "UnexpectedResponseError",
    "Store",
    "NewItemResponse",
]

try:  # Expose runtime package version when installed
    from importlib.metadata import PackageNotFoundError, version

    try:
        __version__ = version("nthesis")
    except PackageNotFoundError:  # pragma: no cover - source checkout
        __version__ = "0.0.0"
except Exception:  # pragma: no cover - extremely defensive
    __version__ = "0.0.0"
