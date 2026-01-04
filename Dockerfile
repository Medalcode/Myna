# Usamos la imagen oficial de Playwright (ya trae Python y los navegadores)
FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy

# Configuración básica
WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Instalar dependencias de Python
COPY faucet_bot/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del proyecto
COPY . .

# Comando de inicio: Lanza el Olimpo
CMD ["python", "olympus.py"]
