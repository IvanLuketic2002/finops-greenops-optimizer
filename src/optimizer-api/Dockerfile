# --- Stage 1: Build zavisnosti ---
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Kreiramo virtualno okruženje (venv)
RUN python -m venv /opt/venv
# Osiguravamo da se svi naredni pip pozivi izvršavaju unutar venv-a
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 2: Finalna minimalna slika ---
FROM python:3.11-slim AS final

WORKDIR /app

# Ažuriramo OS pakete i čistimo keš kako bismo rešili poznate OS ranjivosti
RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# Kopiramo celo virtuelno okruženje iz builder faze
COPY --from=builder /opt/venv /opt/venv

# Kreiramo non-root sistemskog korisnika sa eksplicitnim UID-om radi bezbednosti
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /sbin/nologin appuser

COPY app/ /app/app/

# Postavljamo PATH tako da sistem koristi binarne fajlove iz našeg venv-a
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=/app

# Menjamo vlasništvo nad radnim direktorijumom
RUN chown -R appuser:appgroup /app

# Prebacujemo izvršavanje na bezbednog korisnika
USER 10001

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
