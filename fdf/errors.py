class FdfError(Exception):
    """Base error for FDF files."""


class MapFormatError(FdfError):
    """Raised when a map contains invalid data."""
