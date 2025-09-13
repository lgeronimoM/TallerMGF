FROM python:3.11-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
EXPOSE 5000

# Si tu objeto Flask es 'app' (en app.py)
CMD ["gunicorn","-b","0.0.0.0:5000","app:app"]
