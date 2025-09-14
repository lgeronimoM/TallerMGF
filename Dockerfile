FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_ENV=production \
    PORT=8080

# Usuario no-root
RUN groupadd -r flaskuser && useradd -r -g flaskuser flaskuser

# Directorio de trabajo
WORKDIR /app

# Dependencias del sistema mínimas
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY . .
RUN chown -R flaskuser:flaskuser /app

# Cambiar a usuario no-root
USER flaskuser

# Exponer puerto
EXPOSE 8080

# Health check simple
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

# Usar Flask directamente (más simple y confiable)
CMD ["python", "app.py"]
