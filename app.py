#!/usr/bin/env python
from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mysecret')

# Configuración basada en variables de entorno
class Config:
    # Propiedades host
    SERVER = os.environ.get('SERVER', '0.0.0.0')
    PRTO = int(os.environ.get('PORT', '8080'))
    
    # Propiedades Email
    PMAIL = int(os.environ.get('PMAIL', '587'))
    SMTP = os.environ.get('SMTP', 'smtp.office365.com')
    SEMAIL = os.environ.get('SEMAIL', 'servers@encontrack.com')
    EPASS = os.environ.get('EPASS', '')  # Nunca hardcodear passwords
    REMAIL = os.environ.get('REMAIL', 'luis.geronimo@encontrack.com')
    
    # Debug basado en entorno
    DEBUG = os.environ.get('FLASK_ENV', 'production') == 'development'

# Instancia de configuración
cf = Config()

@app.route('/')
def index():
    return render_template('index.html')

def send_email(subject, body):
    """Función helper para envío de emails"""
    try:
        # Validar que tenemos los datos necesarios
        if not cf.EPASS:
            app.logger.error("Email password not configured")
            return False
            
        # Crear mensaje
        message = MIMEMultipart()
        message["From"] = cf.SEMAIL
        message["To"] = cf.REMAIL
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))
        
        # Enviar email
        context = ssl.create_default_context()
        with smtplib.SMTP(cf.SMTP, cf.PMAIL) as server:
            server.starttls(context=context)
            server.login(cf.SEMAIL, cf.EPASS)
            server.sendmail(cf.SEMAIL, cf.REMAIL, message.as_string())
        
        return True
    except Exception as e:
        app.logger.error(f"Error sending email: {str(e)}")
        return False

@app.route("/agenda", methods=['POST'])
def agendar():
    try:
        # Obtener datos del formulario
        hour = str(request.form.get('hour', ''))
        day = str(request.form.get('day', ''))
        user = str(request.form.get('username', ''))
        telefono = str(request.form.get('telefono', ''))
        email = str(request.form.get('email', ''))
        description = str(request.form.get('descripcion', ''))
        
        # Validar datos requeridos
        if not all([hour, day, user, telefono, email]):
            app.logger.error("Missing required form data")
            return redirect(url_for('index'))
        
        subject = f"Agenda cliente {user}"
        body = (f"El usuario {user} con teléfono {telefono} y su email {email}\n"
               f"Realizó una cita el día {day} en la hora {hour} por el siguiente problema: {description}")
        
        if send_email(subject, body):
            app.logger.info(f"Appointment scheduled for {user}")
        else:
            app.logger.error(f"Failed to send appointment email for {user}")
            
    except Exception as e:
        app.logger.error(f"Error in agendar: {str(e)}")
    
    return redirect(url_for('index'))

@app.route("/mensaje", methods=['POST'])
def mensaje():
    try:
        # Obtener datos del formulario
        user = str(request.form.get('username', ''))
        telefono = str(request.form.get('telefono', ''))
        email = str(request.form.get('email', ''))
        descli = str(request.form.get('descripcion', ''))
        
        # Validar datos requeridos
        if not all([user, telefono, email]):
            app.logger.error("Missing required form data")
            return redirect(url_for('index'))
        
        subject = "Notificación cliente"
        body = (f"El usuario {user} con teléfono {telefono} y su email {email}\n"
               f"Se contactó con usted por el siguiente problema: {descli}")
        
        if send_email(subject, body):
            app.logger.info(f"Message sent for {user}")
        else:
            app.logger.error(f"Failed to send message email for {user}")
            
    except Exception as e:
        app.logger.error(f"Error in mensaje: {str(e)}")
    
    return redirect(url_for('index'))

@app.route('/health')
def health_check():
    """Endpoint para health checks de Kubernetes"""
    return {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }, 200

@app.errorhandler(404)
def not_found(error):
    return render_template('index.html'), 404

@app.errorhandler(500)
def internal_error(error):
    app.logger.error(f"Internal server error: {str(error)}")
    return render_template('index.html'), 500

if __name__ == '__main__':
    app.run(debug=cf.DEBUG, host=cf.SERVER, port=cf.PRTO)
