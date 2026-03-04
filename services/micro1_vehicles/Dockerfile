# Utwórz obraz bazowy
FROM python:3.11-slim
# Ustaw katalog roboczy
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
# lepsze logi w Docker
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Skopiuj plik requirements.txt z wymaganymi bibliotekami
COPY requirements.txt .

# Zainstaluj wymagane biblioteki
RUN pip install --no-cache-dir -r requirements.txt

# Kopiuj potrzebny kod mikroserwisu
COPY src/ ./src/
COPY main.py .
COPY config.env .

# Uruchom mikroserwis
CMD ["python", "main.py"]
