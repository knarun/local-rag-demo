"""
Conversation repository — SQL query operations for the Conversation table.

Responsibilities:
- Insert a new Conversation Turn (session_id, role, content, created_at)
- Retrieve the last N Conversation Turns for a given session_id,
  ordered by created_at ascending (oldest first) to preserve message order for the LLM
- All methods accept a SQLAlchemy Session and execute within the caller's transaction
"""
