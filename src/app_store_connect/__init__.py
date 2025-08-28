"""
App Store Connect API Wrapper

A comprehensive Python wrapper for automating App Store Connect operations.
"""

__version__ = "0.1.0"

from .client import Client
from .auth import Auth
from .exceptions import (
    AppStoreConnectError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
)

__all__ = [
    "Client",
    "Auth",
    "AppStoreConnectError",
    "AuthenticationError",
    "RateLimitError",
    "NotFoundError",
    "ValidationError",
]