"""
SQLAlchemy engine and session factory setup.

Responsibilities:
- Creates the SQLAlchemy engine from the DATABASE_URL in Settings
  exactly once per process (process-wide singleton)
- Creates the SessionFactory (sessionmaker) bound to that engine
  exactly once per process
- Exposes get_db_session() as a FastAPI dependency that yields a
  new SQLAlchemy Session per HTTP request and guarantees it is
  closed (and rolled back on error) when the request finishes

Usage:
- The engine is imported by migrations/migration.py for Base.metadata.create_all()
- get_db_session is imported by dependencies.py to construct per-request repos
- Nothing else should create an engine or session directly

Session lifecycle per request:
    try:
        yield session       # route handler executes here
        session.commit()    # committed only on clean exit
    except:
        session.rollback()  # rolled back on any exception
    finally:
        session.close()     # always closed regardless of outcome
"""
