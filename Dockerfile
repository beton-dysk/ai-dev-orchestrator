FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalacja Gita wewnątrz kontenera (niezbędne do pushowania)
RUN apt-get update && apt-get install -y git && apt-get clean

COPY . .

# Chainlit domyślnie używa portu 8000
EXPOSE 8000

CMD ["chainlit", "run", "app.py", "-w", "--host", "0.0.0.0"]