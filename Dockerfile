FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 8080

# Si tu objeto Flask es 'app' (en app.py)
CMD ["gunicorn","-b","0.0.0.0:8080","app:app"]
