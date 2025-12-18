# BASE IMAGE
FROM python:3.12-slim

WORKDIR /api

# Copy only requirements first for better layer caching
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy application code from our local directory to the working directory
# The first . means the folder we're building from, the second . is whatever is defined in WORKDIR
COPY . .

# Create non-root user for security
RUN adduser --uid 1000 apiuser && chown -R apiuser:apiuser /api
USER apiuser

# Expose doesnt actually do anything other than add some  documentation to some commands
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]