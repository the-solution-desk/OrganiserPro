# Use Python 3.10 slim as the base image
FROM python:3.10-slim AS builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.8.3

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install pip and setuptools
RUN pip install --upgrade pip setuptools wheel

# Copy requirements files
COPY requirements*.txt ./

# Install Python dependencies
RUN pip install --user -r requirements.txt \
    && if [ -f requirements-dev.txt ]; then pip install --user -r requirements-dev.txt; fi

# Copy the rest of the application
COPY . .

# Install the package in development mode
RUN pip install --user -e .

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Set the entrypoint
ENTRYPOINT ["OrganiserPro"]
CMD ["--help"]

# Build a smaller runtime image
FROM python:3.10-slim AS runtime

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy the virtual environment from builder
COPY --from=builder /home/appuser/.local /home/appuser/.local

# Copy the application
COPY --from=builder /app/OrganiserPro /app/OrganiserPro
COPY --from=builder /app/README.md /app/
COPY --from=builder /app/requirements.txt /app/

# Create a non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Add user's .local/bin to PATH
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Set the entrypoint
ENTRYPOINT ["OrganiserPro"]
CMD ["--help"]
