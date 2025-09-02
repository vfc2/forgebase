FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt

# Optional for dev: uncomment if you want dev tools in the image
# RUN pip install --no-cache-dir -r requirements-dev.txt

COPY src ./src
ENV PYTHONPATH=/app/src

EXPOSE 8000
# Use uvicorn directly for clarity; keep reload for dev use
CMD ["python", "src/forgebase/interfaces/web.py"]