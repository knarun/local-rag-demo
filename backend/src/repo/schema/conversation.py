"""
SQLAlchemy ORM definition for the Conversation table.

Columns:
- id         : Integer, primary key, auto-increment
- session_id : String(36), foreign key to session.id, not null, indexed
               Cascade deletes when the parent Session is removed
- role       : Enum('user', 'assistant'), not null — who produced this message
- content    : Text, not null — the message text
- created_at : DateTime, not null, default current UTC timestamp

Relationships:
- Many Conversation Turns belong to one Session

Note:
- Turns are stored in insertion order and retrieved ordered by created_at ascending
  so the LLM always receives history in chronological order
"""
