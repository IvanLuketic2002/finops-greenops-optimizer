# --- Stage 1: Build zavisnosti ---
FROM python:3.11-alpine AS builder

WORKDIR /app

# Alpine koristi apk, instaliramo build-base (zamena za gcc) radi stabilnosti instalacije nekih paketa
RUN apk add --no-cache build-base

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 2: Finalna minimalna slika ---
FROM python:3.11-alpine AS final

WORKDIR /app

# Ažuriramo pakete na Alpine-u da pokupimo sve zakrpe
RUN apk update && apk upgrade --no-cache

COPY --from=builder /opt/venv /opt/venv

# Kreiramo non-root sistemskog korisnika sa eksplicitnim UID-om (Alpine sintaksa)
RUN addgroup -g 10001 appgroup && \
    adduser -u 10001 -G appgroup -h /home/appuser -s /sbin/nologin -D appuser

COPY app/ /app/app/

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=/app

RUN chown -R appuser:appgroup /app

USER 10001

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
