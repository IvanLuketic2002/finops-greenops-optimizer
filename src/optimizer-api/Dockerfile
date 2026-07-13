# --- Stage 1: Build zavisnosti ---
FROM python:3.11-slim AS builder

WORKDIR /app

# slim zahteva minimalno gcc za pojedine pakete
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 2: Finalna minimalna slika ---
FROM python:3.11-slim AS final

WORKDIR /app

# Ažuriramo pakete na Debian slim-u radi bezbednosti OS sloja
RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv

# Kreiramo non-root sistemskog korisnika sa eksplicitnim UID-om
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /sbin/nologin appuser

COPY app/ /app/app/

ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=/app

RUN chown -R appuser:appgroup /app

USER 10001

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
