FROM python:3.11-slim

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production

# Crear usuario no-root para seguridad
RUN groupadd -r flaskuser && useradd -r -g flaskuser flaskuser

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar y instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY . .

# Cambiar propietario de los archivos
RUN chown -R flaskuser:flaskuser /app

# Cambiar a usuario no-root
USER flaskuser

# Exponer puerto
EXPOSE 5000

# Comando de inicio con Gunicorn para producción
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "main:app"]
