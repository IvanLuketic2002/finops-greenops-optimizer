# --- Stage 1: Build zavisnosti ---
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# Instaliramo pakete u lokalni folder .local
RUN pip install --no-cache-dir --user -r requirements.txt

# --- Stage 2: Finalna minimalna slika ---
FROM python:3.11-slim AS final

WORKDIR /app

# Kreiramo non-root sistemskog korisnika sa eksplicitnim UID-om radi bezbednosti
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /sbin/nologin appuser

# Kopiramo instalirane Python pakete i aplikaciju iz builder-a
COPY --from=builder /root/.local /home/appuser/.local
COPY app/ /app/app/

# Postavljamo varijable okruženja tako da Python vidi instalirane pakete
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/app

# Menjamo vlasništvo nad radnim direktorijumom
RUN chown -R appuser:appgroup /app

# Prebacujemo izvršavanje na bezbednog korisnika
USER 10001

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
