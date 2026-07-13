FROM python:3.11-slim

WORKDIR /app

# 1. Ažuriramo pakete na OS nivou radi bezbednosti (Trivy patch)
RUN apt-get update && \
    apt-get upgrade -y && \
    rm -rf /var/lib/apt/lists/*

# 2. Kopiramo requirements i instaliramo zavisnosti direktno
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Kreiramo non-root sistemskog korisnika sa eksplicitnim UID-om
RUN groupadd -g 10001 appgroup && \
    useradd -u 10001 -g appgroup -m -s /sbin/nologin appuser

# 4. Kopiramo aplikaciju i postavljamo vlasništvo
COPY app/ /app/app/
RUN chown -R appuser:appgroup /app

# 5. Prebacujemo izvršavanje na bezbednog korisnika
USER 10001

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
