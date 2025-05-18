from flask_sqlalchemy import SQLAlchemy
from datetime import datetime # Para usar datas

db = SQLAlchemy() # Instância do SQLAlchemy, será inicializada no __init__.py

class Aluno(db.Model):
    __tablename__ = 'aluno'
    ID_Aluno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Nome = db.Column(db.String(120), nullable=False)
    Endereco = db.Column(db.String(200), nullable=True)
    Cidade = db.Column(db.String(80), nullable=True)
    Estado = db.Column(db.String(2), nullable=True) # UF com 2 caracteres
    Telefone = db.Column(db.String(20), nullable=True)
    Data_Matricula = db.Column(db.Date, nullable=True)
    Data_Desligamento = db.Column(db.Date, nullable=True)
    Data_Vencimento = db.Column(db.Date, nullable=True)

    # Relacionamento com Pagamento: um aluno pode ter vários pagamentos
    # 'backref' cria um atributo 'aluno' em Pagamento para acessar o aluno associado
    # 'lazy=True' significa que os pagamentos serão carregados quando acessados
    pagamentos = db.relationship('Pagamento', backref='aluno', lazy=True)

    def __repr__(self):
        return f'<Aluno {self.ID_Aluno}: {self.Nome}>'

    # Método para serializar o objeto para JSON (útil para APIs)
    def to_dict(self):
        return {
            'ID_Aluno': self.ID_Aluno,
            'Nome': self.Nome,
            'Endereco': self.Endereco,
            'Cidade': self.Cidade,
            'Estado': self.Estado,
            'Telefone': self.Telefone,
            'Data_Matricula': self.Data_Matricula.isoformat() if self.Data_Matricula else None,
            'Data_Desligamento': self.Data_Desligamento.isoformat() if self.Data_Desligamento else None,
            'Data_Vencimento': self.Data_Vencimento.isoformat() if self.Data_Vencimento else None
        }

class Pagamento(db.Model):
    __tablename__ = 'pagamento'
    ID_Pagamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ID_Aluno = db.Column(db.Integer, db.ForeignKey('aluno.ID_Aluno'), nullable=False)
    Data = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    Valor = db.Column(db.Float, nullable=False)
    Tipo = db.Column(db.String(10), nullable=False) # "dinheiro" ou "cartão"

    def __repr__(self):
        return f'<Pagamento {self.ID_Pagamento} - Aluno {self.ID_Aluno}>'

    # Método para serializar o objeto para JSON
    def to_dict(self):
        return {
            'ID_Pagamento': self.ID_Pagamento,
            'ID_Aluno': self.ID_Aluno,
            'Data': self.Data.isoformat() if self.Data else None,
            'Valor': self.Valor,
            'Tipo': self.Tipo
        }