"""
FastAPI application entry point.

Responsibilities:
- Creates the FastAPI app instance
- Registers all routers (ingest, query, chat, document)
- Registers global exception handlers from utils/exception_handler.py
- Runs the database migration (Base.metadata.create_all) on application startup
- Configures CORS middleware for the React frontend
- Handles application startup and shutdown lifecycle events
"""
