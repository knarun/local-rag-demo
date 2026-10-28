"""
Global FastAPI exception handlers.

Responsibilities:
- Registers exception handlers on the FastAPI app instance in main.py
- AppException handler     : Catches all AppException instances raised by services,
                              logs the error code + message + request path + request UUID
                              at ERROR level, and returns a JSON error response
- RequestValidationError handler : Catches Pydantic validation errors from request parsing,
                                   logs at WARNING level, and returns a JSON error response
                                   with VALIDATION_ERROR code and per-field details
- Generic Exception handler : Catches all unhandled exceptions, logs the full stack trace
                              at CRITICAL level, and returns a JSON 500 response

Error response shape (all handlers):
{
    "error_code": "<ErrorCode string>",
    "message": "<human-readable description>",
    "details": <object or null>
}
"""
