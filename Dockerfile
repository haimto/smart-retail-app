# ==========================================
# STAGE 1: Builder
# ==========================================
FROM python:3.14-slim AS builder

WORKDIR /app

COPY requirements.txt .

# FIX 1: Removed --no-deps so psycopg[binary] and other sub-dependencies actually download
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt gunicorn

# ==========================================
# STAGE 2: Runner
# ==========================================
FROM python:3.14-slim AS runner

WORKDIR /app

# FIX 2: Added libpq5 just in case psycopg falls back to the C wrapper
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y libpq5 && \
    rm -rf /var/lib/apt/lists/*

# FIX 3: Changed -M to -m to create a home directory, preventing Gunicorn permission errors
RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g appgroup -s /sbin/nologin -m appuser

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache /wheels/*

COPY app/ ./app/
COPY init_db.py .

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 5000

CMD ["gunicorn", "--workers", "2", "--bind", "0.0.0.0:5000", "app:create_app()"]
