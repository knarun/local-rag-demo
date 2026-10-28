"""
Database migration runner — startup table creation.

Responsibilities:
- Imports all ORM schema definitions (document, chunk, session, conversation)
  to ensure they are registered with Base.metadata before create_all is called
- Calls Base.metadata.create_all(bind=engine) to create all tables that do not
  already exist — idempotent, safe to run on every startup
- Does nothing if all tables already exist
- Raises and logs an error if table creation fails, halting application startup

Usage:
- Called once during the FastAPI lifespan startup event in main.py
- Does not use Alembic — schema changes require a new migration file or
  manual table alteration for production deployments
"""
