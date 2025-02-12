# Use the official Python 3.12 image
FROM python:3.12

# Set environment variables to prevent Python from writing .pyc files and ensure UTF-8 encoding
ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=UTF-8

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry for dependency management
RUN pip install --no-cache-dir poetry

# Copy only dependency files first (for better caching)
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry (without installing the root package)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application files
COPY . .

# Expose the port FastAPI will run on
EXPOSE 8000

# Set the command to run the FastAPI app
CMD ["poetry", "run", "uvicorn", "run:app", "--host", "127.0.0.1", "--port", "8000", "--reload"]
