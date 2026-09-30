class MemberAlreadyExistsError(Exception):
    """Raised when attempting to join an existing tracker membership."""

class InvalidTimezoneError(Exception):
    """Raised when a tracker member provides an invalid timezone."""

class MemberNotFoundError(Exception):
    """Raised when a tracker member cannot be found."""
