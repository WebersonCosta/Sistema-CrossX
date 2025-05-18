from flask import Flask
from .models import db # Importa a instância db de models.py
from config import Config # Importa a classe de configuração

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class) # Carrega as configurações do objeto Config

    # Inicializa o SQLAlchemy com a aplicação Flask
    db.init_app(app)

    # Importa e registra o Blueprint das rotas
    # Fazemos a importação aqui para evitar importações circulares
    from .routes import api_bp
    app.register_blueprint(api_bp) # O url_prefix já está definido no Blueprint

    from .routes import web
    app.register_blueprint(web)

    # Cria as tabelas no banco de dados, se não existirem
    # Isso é feito dentro do contexto da aplicação
    with app.app_context():
        db.create_all() # ATENÇÃO: Em produção, você usaria migrações (Flask-Migrate)

    return app