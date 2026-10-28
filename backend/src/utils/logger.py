"""
Loguru logger setup.

Responsibilities:
- Configures the Loguru logger with the log level defined in Settings (default: INFO)
- Sets output format to include: timestamp, log level, module name, and message
- Exposes a single `logger` instance imported by all other modules
- Called once at application startup (main.py)
"""
