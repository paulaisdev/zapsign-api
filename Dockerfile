FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev curl && rm -rf /var/lib/apt/lists/*

# Instalar dockerize
RUN curl -L https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz | tar -C /usr/local/bin -xzv

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

# Esperar o banco de dados ficar disponível
CMD ["dockerize", "-wait", "tcp://db:5432", "-timeout", "20s", "python", "manage.py", "runserver", "0.0.0.0:8000"]
