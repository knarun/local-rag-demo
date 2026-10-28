"""
Custom application exception classes.

Classes:
- AppException       : Base class for all application-level exceptions
                       Carries an ErrorCode enum value, a human-readable message,
                       an HTTP status code, and an optional details dict
- ValidationException: Raised when request input fails business-rule validation
                       (distinct from Pydantic schema validation, which is automatic)

Usage:
- Services raise AppException (or subclasses) with the appropriate ErrorCode
- exception_handler.py catches AppException and maps it to a JSON error response
"""
