"""
Shared utility helper functions.

Functions:
- sanitize_filename(filename: str) -> str
    Strips path components and special characters from an uploaded filename.
    Used by Ingest_Service before storing the filename in the database.

- compute_sha256(data: str | bytes) -> str
    Returns a hex SHA-256 hash of the input. Used by Cache_Client to build
    deterministic, fixed-length cache keys from query text and embedding vectors.

- serialize_embedding(vector: list[float]) -> bytes
    Converts a float list to a deterministic byte sequence (fixed precision,
    fixed byte order) for consistent hashing in Cache_Client.build_key().

- generate_uuid() -> str
    Returns a new UUID4 string (36 characters). Used by Chat_Service
    when creating a new Session.
"""
