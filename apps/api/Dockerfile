FROM python:3.12-slim

WORKDIR /app

# Copy pyproject.toml and poetry.lock from the root
COPY pyproject.toml poetry.lock ./

# Install poetry and dependencies (without the root project)
RUN pip install poetry && poetry config virtualenvs.create false \
 && poetry install --only=main --no-root

# Copy the API application code
COPY apps/api/ .

# Expose port 8000
EXPOSE 8000

# Start the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
