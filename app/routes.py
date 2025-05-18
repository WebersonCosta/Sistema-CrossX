from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import db, Aluno, Pagamento
from .api_routes import api_bp  # Importar o Blueprint da API

# Blueprint para as rotas da interface web
web = Blueprint('web', __name__)

@web.route('/')
def index():
    return render_template('index.html')

# --- ROTAS PARA ALUNOS ---
@web.route('/alunos')
def listar_alunos():
    alunos = Aluno.query.all()
    return render_template('alunos/lista.html', alunos=alunos)

@web.route('/alunos/novo')
def novo_aluno_form():
    return render_template('alunos/novo.html')

@web.route('/alunos/<int:id_aluno>')
def detalhes_aluno(id_aluno):
    aluno = Aluno.query.get_or_404(id_aluno, description=f"Aluno com ID {id_aluno} não encontrado")
    pagamentos = Pagamento.query.filter_by(ID_Aluno=id_aluno).all()
    return render_template('alunos/detalhes.html', aluno=aluno, pagamentos=pagamentos)