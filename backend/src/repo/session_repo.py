"""
Session repository — SQL query operations for the Session table.

Responsibilities:
- Create a new Session record with a UUID primary key and current UTC timestamp
- Get a Session record by session_id string
- All methods accept a SQLAlchemy Session and execute within the caller's transaction
"""
