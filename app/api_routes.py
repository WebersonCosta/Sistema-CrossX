from flask import Blueprint, request, jsonify
from .models import db, Aluno, Pagamento
from datetime import datetime

# Blueprint para as rotas da API
api_bp = Blueprint('api_bp', __name__, url_prefix='/api')

@api_bp.route('/')
def hello_world():
    return jsonify(message="Ola, API do CrossX Funcionando!")

# --- ROTAS PARA ALUNOS ---
@api_bp.route('/alunos', methods=['POST'])
def criar_aluno():
    dados = request.get_json()

    # Validação básica dos dados
    if not dados or not dados.get('Nome'):
        return jsonify({'erro': 'O nome do aluno é obrigatório'}), 400

    try:
        data_matricula = datetime.strptime(dados.get('Data_Matricula'), '%Y-%m-%d').date() if dados.get('Data_Matricula') else None
        data_vencimento = datetime.strptime(dados.get('Data_Vencimento'), '%Y-%m-%d').date() if dados.get('Data_Vencimento') else None
    except (ValueError, TypeError):
        return jsonify({'erro': 'Formato de data inválido para Data_Matricula ou Data_Vencimento. Use YYYY-MM-DD.'}), 400

    novo_aluno = Aluno(
        Nome=dados.get('Nome'),
        Endereco=dados.get('Endereco'),
        Cidade=dados.get('Cidade'),
        Estado=dados.get('Estado'),
        Telefone=dados.get('Telefone'),
        Data_Matricula=data_matricula,
        Data_Vencimento=data_vencimento
        # Data_Desligamento será nula por padrão ao criar
    )
    db.session.add(novo_aluno)
    db.session.commit()
    return jsonify(novo_aluno.to_dict()), 201  # 201 Created

@api_bp.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = Aluno.query.all()
    return jsonify([aluno.to_dict() for aluno in alunos]), 200

@api_bp.route('/alunos/<int:id_aluno>', methods=['GET'])
def obter_aluno(id_aluno):
    aluno = Aluno.query.get_or_404(id_aluno, description=f"Aluno com ID {id_aluno} não encontrado")
    return jsonify(aluno.to_dict()), 200

@api_bp.route('/alunos/<int:id_aluno>', methods=['PUT'])
def atualizar_aluno(id_aluno):
    aluno = Aluno.query.get_or_404(id_aluno, description=f"Aluno com ID {id_aluno} não encontrado")
    dados = request.get_json()
    
    if not dados:
        return jsonify({'erro': 'Nenhum dado fornecido para atualização'}), 400
    
    # Atualizar campos se fornecidos
    if 'Nome' in dados:
        aluno.Nome = dados['Nome']
    if 'Endereco' in dados:
        aluno.Endereco = dados['Endereco']
    if 'Cidade' in dados:
        aluno.Cidade = dados['Cidade']
    if 'Estado' in dados:
        aluno.Estado = dados['Estado']
    if 'Telefone' in dados:
        aluno.Telefone = dados['Telefone']
    
    # Campos de data requerem conversão
    if 'Data_Matricula' in dados:
        try:
            aluno.Data_Matricula = datetime.strptime(dados['Data_Matricula'], '%Y-%m-%d').date() if dados['Data_Matricula'] else None
        except ValueError:
            return jsonify({'erro': 'Formato de data inválido para Data_Matricula. Use YYYY-MM-DD.'}), 400
    
    if 'Data_Vencimento' in dados:
        try:
            aluno.Data_Vencimento = datetime.strptime(dados['Data_Vencimento'], '%Y-%m-%d').date() if dados['Data_Vencimento'] else None
        except ValueError:
            return jsonify({'erro': 'Formato de data inválido para Data_Vencimento. Use YYYY-MM-DD.'}), 400
    
    if 'Data_Desligamento' in dados:
        try:
            aluno.Data_Desligamento = datetime.strptime(dados['Data_Desligamento'], '%Y-%m-%d').date() if dados['Data_Desligamento'] else None
        except ValueError:
            return jsonify({'erro': 'Formato de data inválido para Data_Desligamento. Use YYYY-MM-DD.'}), 400
    
    db.session.commit()
    return jsonify(aluno.to_dict()), 200

@api_bp.route('/alunos/<int:id_aluno>', methods=['DELETE'])
def excluir_aluno(id_aluno):
    aluno = Aluno.query.get_or_404(id_aluno, description=f"Aluno com ID {id_aluno} não encontrado")
    db.session.delete(aluno)
    db.session.commit()
    return jsonify({'mensagem': f'Aluno com ID {id_aluno} excluído com sucesso'}), 200

# Rota para desligar um aluno (sem excluir)
@api_bp.route('/alunos/<int:id_aluno>/desligar', methods=['POST'])
def desligar_aluno(id_aluno):
    try:
        aluno = Aluno.query.get_or_404(id_aluno, description=f"Aluno com ID {id_aluno} não encontrado")

        dados = request.get_json() or {}

        try:
            data_desligamento = datetime.strptime(
                dados.get('Data_Desligamento'), '%Y-%m-%d'
            ).date() if dados.get('Data_Desligamento') else datetime.now().date()
        except ValueError:
            return jsonify({'erro': 'Formato de data inválido para Data_Desligamento. Use YYYY-MM-DD.'}), 400

        aluno.Data_Desligamento = data_desligamento
        db.session.commit()

        return jsonify({
            'mensagem': f'Aluno {aluno.Nome} desligado com sucesso',
            'aluno': aluno.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'erro': 'Erro interno no servidor', 'detalhes': str(e)}), 500


# --- ROTAS PARA PAGAMENTOS ---
@api_bp.route('/alunos/<int:id_aluno>/pagamentos', methods=['GET'])
def listar_pagamentos_aluno(id_aluno):
    # Verifica se o aluno existe
    aluno = Aluno.query.get_or_404(id_aluno, description=f"Aluno com ID {id_aluno} não encontrado")
    
    # Obtém todos os pagamentos do aluno
    pagamentos = Pagamento.query.filter_by(ID_Aluno=id_aluno).all()
    
    return jsonify([pagamento.to_dict() for pagamento in pagamentos]), 200

@api_bp.route('/alunos/<int:id_aluno>/pagamentos', methods=['POST'])
def criar_pagamento_para_aluno(id_aluno):
    aluno = Aluno.query.get_or_404(id_aluno, description=f"Aluno com ID {id_aluno} não encontrado para adicionar pagamento")
    dados = request.get_json()

    if not dados or dados.get('Valor') is None or not dados.get('Tipo'):
        return jsonify({'erro': 'Valor e Tipo do pagamento são obrigatórios'}), 400

    if dados.get('Tipo') not in ['dinheiro', 'cartão']:
        return jsonify({'erro': 'Tipo de pagamento inválido. Use "dinheiro" ou "cartão".'}), 400

    try:
        data_pagamento = datetime.strptime(dados.get('Data'), '%Y-%m-%d').date() if dados.get('Data') else datetime.now().date()
        valor_pagamento = float(dados.get('Valor'))
    except (ValueError, TypeError):
        return jsonify({'erro': 'Formato de Data ou Valor inválido. Data: YYYY-MM-DD, Valor: número.'}), 400

    novo_pagamento = Pagamento(
        ID_Aluno=aluno.ID_Aluno,
        Data=data_pagamento,
        Valor=valor_pagamento,
        Tipo=dados.get('Tipo')
    )
    db.session.add(novo_pagamento)
    db.session.commit()
    return jsonify(novo_pagamento.to_dict()), 201

@api_bp.route('/pagamentos/<int:id_pagamento>', methods=['GET'])
def obter_pagamento(id_pagamento):
    pagamento = Pagamento.query.get_or_404(id_pagamento, description=f"Pagamento com ID {id_pagamento} não encontrado")
    return jsonify(pagamento.to_dict()), 200

@api_bp.route('/pagamentos/<int:id_pagamento>', methods=['DELETE'])
def excluir_pagamento(id_pagamento):
    pagamento = Pagamento.query.get_or_404(id_pagamento, description=f"Pagamento com ID {id_pagamento} não encontrado")
    db.session.delete(pagamento)
    db.session.commit()
    return jsonify({'mensagem': f'Pagamento com ID {id_pagamento} excluído com sucesso'}), 200