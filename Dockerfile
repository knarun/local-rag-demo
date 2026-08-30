# Use a slim, official Python base image to keep the container small
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Install uv (the same package manager you use locally)
RUN pip install --no-cache-dir uv

# Copy dependency files first (better Docker layer caching:
# dependencies only reinstall if pyproject.toml/uv.lock actually change)
COPY pyproject.toml uv.lock ./

# Install dependencies exactly as locked, skipping dev-only tools
# (creates a .venv inside the container, same as it would locally)
RUN uv sync --frozen --no-dev

# Make the container's Python use that .venv automatically,
# so plain "python" commands below find the installed packages
ENV PATH="/app/.venv/bin:$PATH"

# Now copy the rest of the project code into the container
COPY . .

# Default command when the container starts.
# Update this once query.py / ingest.py exist.
CMD ["python", "query.py"]
