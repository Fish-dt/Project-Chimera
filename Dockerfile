# Use a lightweight Python base image
FROM python:3.12-slim

# Install the 'uv' binary directly from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory inside the container
WORKDIR /app

# Copy dependency files first to utilize Docker layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies into the container
RUN uv sync --frozen --no-install-project

# Copy your actual project files (CSVs, scripts, etc.)
COPY . .

# Final sync to include project code
RUN uv sync --frozen

# Default command: Run the pytest suite
CMD ["uv", "run", "pytest"]