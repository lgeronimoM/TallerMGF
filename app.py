import os
import json
from datetime import datetime
from flask import Flask

app = Flask(__name__)

@app.get("/health")
def health():
    """Enhanced health check"""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.1",
        "environment": os.environ.get('FLASK_ENV', 'production')
    }, 200

@app.get("/")
def hello():
    """Enhanced welcome message"""
    return {
        "message": "Hello TallerMGF!",
        "version": "1.0.1", 
        "timestamp": datetime.utcnow().isoformat(),
        "author": "Luis Geronimo",
        "endpoints": {
            "health": "/health - Health check",
            "info": "/info - App information", 
            "status": "/status - Simple status"
        }
    }, 200

@app.get("/info")
def info():
    """Application information"""
    return {
        "application": "TallerMGF",
        "version": "1.0.1",
        "description": "Enhanced Flask application", 
        "author": "Luis Geronimo",
        "environment": os.environ.get('FLASK_ENV', 'production'),
        "timestamp": datetime.utcnow().isoformat()
    }, 200

@app.get("/status") 
def status():
    """Simple status endpoint"""
    return {
        "status": "operational",
        "version": "1.0.1", 
        "timestamp": datetime.utcnow().isoformat()
    }, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
