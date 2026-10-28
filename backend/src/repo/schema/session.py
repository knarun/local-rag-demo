"""
SQLAlchemy ORM definition for the Session table.

Columns:
- id         : String(36), primary key — the UUID session_id assigned at session creation
- created_at : DateTime, not null, default current UTC timestamp

Relationships:
- One Session has many Conversation Turns (cascade delete on session removal)

Note:
- A Session record is persisted immediately when a new chat is started,
  independent of whether the subsequent LLM call succeeds (see chat_service.py)
"""
