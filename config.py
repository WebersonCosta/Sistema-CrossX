import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Configuração do Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'chave-secreta-desenvolvimento'
    DEBUG = True
    
    # Configuração do SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'crossx.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuração do Flask-WTF
    WTF_CSRF_ENABLED = True
    
    # Configuração do JSON
    JSON_AS_ASCII = False
    JSONIFY_PRETTYPRINT_REGULAR = True