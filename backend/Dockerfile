# SidiWeb Backend (FastAPI)
FROM python:3.11-slim

WORKDIR /app

# libmagic is required by python-magic (image validation)
RUN apt-get update \
    && apt-get install -y --no-install-recommends libmagic1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Uploads live here (mounted as a volume in compose)
RUN mkdir -p src/media/uploads

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
