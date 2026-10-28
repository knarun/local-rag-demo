"""
SQLAlchemy declarative base.

Responsibilities:
- Defines the single shared DeclarativeBase instance used by all ORM table definitions
- Imported by document.py, chunk.py, session.py, and conversation.py schema files
- Imported by the migration module to run Base.metadata.create_all()
"""
