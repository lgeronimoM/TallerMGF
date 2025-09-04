# Dockerfile
FROM python:3.11-slim


# Optimiza builds y evita bytecode files
ENV PYTHONDONTWRITEBYTECODE=1 \
PYTHONUNBUFFERED=1 \
PIP_NO_CACHE_DIR=1


# Instala dependencias del sistema (si tu app las requiere, añade aquí)
RUN apt-get update && apt-get install -y --no-install-recommends \
build-essential \
&& rm -rf /var/lib/apt/lists/*


# Crea user no root
RUN useradd -m appuser
WORKDIR /app


# Requisitos primero para mejor cache
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt && pip install gunicorn


# Copia código
COPY . /app


# Puerto interno
EXPOSE 8000


# Ajusta si tu app se instancia distinto; asumo app Flask en main.py exporta `app`
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "--workers", "2", "--threads", "4", "--timeout", "60"]
