FROM python:3.11-slim

# Set working directory
WORKDIR /workspace

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run Alembic migrations before starting the app
# This ensures DB schema is always up-to-date
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000