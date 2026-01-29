# Version logera de python.
FROM python:3.11-slim

# Establecemos la carpeta de trabajo dentro del contenedor
WORKDIR /app

# Instalamos dependencias del sistema necesarias para compilar (por seguridad)
RUN apt-get update && apt-get install -y default-libmysqlclient-dev build-essential pkg-config && rm -rf /var/lib/apt/lists/*

# Copiamos los requisitos e instalamos las librerias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el codigo fuente de la carpeta src
COPY src/ ./src/

# Informamos de que la app usa el puerto 8000
EXPOSE 8000

# Comando para arrancar la aplicacion al iniciar el contenedor
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]