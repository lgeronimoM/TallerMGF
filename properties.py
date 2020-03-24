__author__ = 'Luis Geronimo'
class Config(object):
    #propiedades host
    SERVER='0.0.0.0'
    PRTO = 8080

    #propiedaeds Email
    PMAIL = 587  # For starttls
    SMTP = "smtp.office365.com"
    SEMAIL = "servers@encontrack.com"
    EPASS = "Tav76551"
    REMAIL ="luis.geronimo@encontrack.com"

class ProductionConfig(Config):
    DEBUG=False

class DevelopmentConfig(Config):
    DEBUG=True
