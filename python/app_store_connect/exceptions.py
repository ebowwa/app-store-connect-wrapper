"""
Custom exceptions for App Store Connect API wrapper
"""


class AppStoreConnectError(Exception):
    """Base exception for all App Store Connect errors"""
    pass


class AuthenticationError(AppStoreConnectError):
    """Raised when authentication fails"""
    pass


class RateLimitError(AppStoreConnectError):
    """Raised when API rate limit is exceeded"""
    pass


class NotFoundError(AppStoreConnectError):
    """Raised when a resource is not found"""
    pass


class ValidationError(AppStoreConnectError):
    """Raised when validation fails"""
    pass


class ConflictError(AppStoreConnectError):
    """Raised when there's a conflict (e.g., duplicate name)"""
    pass