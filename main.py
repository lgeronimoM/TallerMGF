#!/usr/bin/env python
from flask import Flask, render_template, redirect, url_for, request
from flask_environments import Environments

import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
if app.config["ENV"] == "production":
    app.config.from_object("properties.ProductionConfig")
elif app.config["ENV"] == "development":
    app.config.from_object("properties.DevelopmentConfig")
else:
    app.config.from_object("properties.TestingConfig")

class cf():
    SERVER=app.config["SERVER"]
    PTO=app.config["PRTO"]
    DEBUG=app.config["DEBUG"]
    PMAIL=app.config["PMAIL"]
    SMTP=app.config["SMTP"]
    SEMAIL=app.config["SEMAIL"]
    REMAIL=app.config["REMAIL"]
    EPASS=app.config["EPASS"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/agenda", methods=['POST'])
def agendar():
    hour= str(request.form['hour'])
    day= str(request.form['day'])
    user = str(request.form['username'])
    telefono = str(request.form['telefono'])
    email = str(request.form['email'])
    description = str(request.form['descripcion'])

    port = cf.PMAIL
    smtp_server = cf.SMTP
    sender_email = cf.SEMAIL
    receiver_email = cf.REMAIL
    password = cf.EPASS
    subject = "Agenda cliente " + user
    body = "El usuario "+user+" con telefono "+telefono+" y su email "+email+"\nRelizo una cita el dia "+day+" en la hora "+hour+" por el siguiente problema: "+description
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    return redirect(url_for('index'))

@app.route("/mensaje", methods=['POST'])
def mensaje():
    user = str(request.form['username'])        
    telefono = str(request.form['telefono'])
    email = str(request.form['email'])
    descli = str(request.form['descripcion'])

    port = cf.PMAIL
    smtp_server = cf.SMTP
    sender_email = cf.SEMAIL
    receiver_email = cf.REMAIL
    password = cf.EPASS
    subject = "Notificación cliente"
    body = "El usario "+user+" con telefono "+telefono+" y su email "+email+"\nSe contacto con usted por el siguiente problema: "+descli
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()
    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    return redirect(url_for('index'))

@app.route('/health')
def health_check():
    """Endpoint para health checks de Kubernetes"""
    return {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }, 200
    
if __name__ == '__main__':
    app.run(debug = cf.DEBUG, host=cf.SERVER, port = cf.PTO )
