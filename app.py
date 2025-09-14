import os
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
import psutil
import platform

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['ENV'] = os.environ.get('FLASK_ENV', 'production')
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'

# Enable CORS
CORS(app)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': 'The requested resource was not found',
        'status_code': 404
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f'Internal Server Error: {str(error)}')
    return jsonify({
        'error': 'Internal Server Error',
        'message': 'An unexpected error occurred',
        'status_code': 500
    }), 500

# Request logging middleware
@app.before_request
def log_request_info():
    logger.info(f'{request.method} {request.url} - IP: {request.remote_addr}')

# Original endpoints (mejorados)
@app.get("/health")
def health():
    """Enhanced health check with system metrics"""
    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        health_data = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0',
            'environment': app.config.get('ENV'),
            'system': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'disk_percent': round((disk.used / disk.total) * 100, 2),
                'platform': platform.platform()
            }
        }
        
        # Check if system is under stress
        if cpu_percent > 90 or memory.percent > 90:
            health_data['status'] = 'degraded'
            return jsonify(health_data), 503
            
        return jsonify(health_data), 200
        
    except Exception as e:
        logger.error(f'Health check failed: {str(e)}')
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 503

@app.get("/")
def hello():
    """Enhanced welcome endpoint"""
    return jsonify({
        'message': 'Hello TallerMGF!',
        'version': '1.0.0',
        'environment': app.config.get('ENV'),
        'timestamp': datetime.utcnow().isoformat(),
        'author': 'Luis Geronimo',
        'description': 'Enhanced Flask application with monitoring',
        'endpoints': {
            'health': '/health - System health check',
            'info': '/info - Application information',
            'metrics': '/metrics - System metrics',
            'status': '/status - API status'
        }
    }), 200

# New useful endpoints
@app.get("/info")
def info():
    """Application information"""
    return jsonify({
        'application': 'TallerMGF',
        'version': '1.0.0',
        'description': 'Enhanced Flask application with monitoring',
        'author': 'Luis Geronimo',
        'python_version': platform.python_version(),
        'flask_version': '3.0.0',
        'environment': app.config.get('ENV'),
        'debug_mode': app.config.get('DEBUG'),
        'platform': {
            'system': platform.system(),
            'node': platform.node(),
            'release': platform.release(),
            'machine': platform.machine()
        },
        'timestamp': datetime.utcnow().isoformat()
    }), 200

@app.get("/metrics")
def metrics():
    """System metrics endpoint"""
    try:
        cpu = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return jsonify({
            'metrics': {
                'cpu': {
                    'percent': cpu,
                    'count': psutil.cpu_count()
                },
                'memory': {
                    'total_gb': round(memory.total / (1024**3), 2),
                    'available_gb': round(memory.available / (1024**3), 2),
                    'used_gb': round(memory.used / (1024**3), 2),
                    'percent': memory.percent
                },
                'disk': {
                    'total_gb': round(disk.total / (1024**3), 2),
                    'used_gb': round(disk.used / (1024**3), 2),
                    'free_gb': round(disk.free / (1024**3), 2),
                    'percent': round((disk.used / disk.total) * 100, 2)
                }
            },
            'timestamp': datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        logger.error(f'Metrics collection failed: {str(e)}')
        return jsonify({
            'error': 'Failed to collect metrics',
            'message': str(e)
        }), 500

@app.get("/status")
def status():
    """API status endpoint"""
    uptime_seconds = int((datetime.now() - datetime.fromtimestamp(psutil.boot_time())).total_seconds())
    uptime_hours = uptime_seconds // 3600
    uptime_minutes = (uptime_seconds % 3600) // 60
    
    return jsonify({
        'api_status': 'operational',
        'version': '1.0.0',
        'uptime': f'{uptime_hours}h {uptime_minutes}m',
        'requests_processed': 'tracking not implemented',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

# Kubernetes probes (simples)
@app.get("/ready")
def ready():
    """Readiness probe for Kubernetes"""
    return jsonify({'status': 'ready'}), 200

@app.get("/live")
def live():
    """Liveness probe for Kubernetes"""
    return jsonify({'status': 'alive'}), 200

# Testing endpoint
@app.post("/echo")
def echo():
    """Echo endpoint for testing"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    return jsonify({
        'echo': data,
        'method': request.method,
        'timestamp': datetime.utcnow().isoformat(),
        'client_ip': request.remote_addr
    }), 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    host = os.environ.get('HOST', '0.0.0.0')
    debug = os.environ.get('FLASK_DEBUG', 'false').lower() == 'true'
    
    logger.info(f"Starting TallerMGF application on {host}:{port}")
    logger.info(f"Debug mode: {debug}")
    logger.info(f"Environment: {os.environ.get('FLASK_ENV', 'production')}")
    
    app.run(host=host, port=port, debug=debug)
