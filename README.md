# Guia de Instalação e Teste do Sistema CrossX
Este guia fornecerá instruções detalhadas sobre como configurar, instalar e testar o sistema CrossX. Este documento é destinado aos professores avaliadores do projeto.

## Sumário
- [Visao Geral do Projeto](#visao-geral-do-projeto)
- [Pre-requisitos](#pre-requisitos)
- [Instalacao](#instalacao)
- [Configuracao](#configuracao)
- [Execucao do Sistema](#execucao-do-sistema)
- [Testando o Sistema](#testando-o-sistema)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [API Documentation](#api-documentation)
- [Troubleshooting](#troubleshooting)

## Visao Geral do Projeto
O **CrossX** é um sistema de gerenciamento para academias, permitindo o cadastro de alunos e o registro de pagamentos. O sistema possui uma interface web e uma API REST para manipulação dos dados.

### Principais Funcionalidades
- Cadastro, visualização e atualização de alunos

- Registro de pagamentos por aluno

- Desligamento de alunos

- API REST para integração com outros sistemas

## Pre-requisitos
- Python 3.8 ou superior

- pip (gerenciador de pacotes do Python)

- Navegador web moderno (Chrome, Firefox, Edge, etc.)

## Instalacao
1. Clone ou descompacte o projeto
Se estiver recebendo o projeto como um arquivo compactado, descompacte-o em uma pasta de sua preferência.

2. Crie um ambiente virtual Python
Navegue até a pasta do projeto e execute:

### No Windows
```

  python -m venv venv

```
### No macOS/Linux

```

python3 -m venv venv

```
3. Ative o ambiente virtual

- No Windows
```
venv\Scripts\activate

```
- No macOS/Linux
  
```

source venv/bin/activate

```
4. Instale as dependências

```

pip install Flask Flask-SQLAlchemy

```
## Configuracao
### Variáveis de Ambiente (Opcional)
O sistema já está configurado para funcionar com valores padrão, mas você pode personalizar as seguintes variáveis:

- SECRET_KEY: Chave de segurança para o Flask

- DATABASE_URL: URL do banco de dados (padrão: SQLite local)

### No Windows:

```

set SECRET_KEY=sua-chave-secreta

```

### No macOS/Linux:


```

export SECRET_KEY=sua-chave-secreta

```
## Execucao do Sistema
1. Ative o ambiente virtual (se ainda não estiver ativo)

- No Windows
```

venv\Scripts\activate

```

- No macOS/Linux

```

source venv/bin/activate

```

2. Execute o servidor

```

python run.py

```
3. Acesse o sistema no navegador

http://localhost:5000

## Testando o Sistema
### Interface Web
- **Página Inicial:** http://localhost:5000

- **Listagem de Alunos:** Clique em "Ver Alunos"

- **Cadastro de Aluno:** Clique em "Novo Aluno"

- **Detalhes do Aluno:** Clique em "Detalhes" após o cadastro

- **Registro de Pagamento:** Clique em "Novo Pagamento"

- **Edição de Aluno:** Clique em "Editar Dados"

- **Desligamento de Aluno:** Clique em "Desligar Aluno"

### Testando a API
- **Verificação da API:** http://localhost:5000/api/

- **Listagem de Alunos:** http://localhost:5000/api/alunos

- **Cadastro de Aluno via curl:**
```

curl -X POST http://localhost:5000/api/alunos \
  -H "Content-Type: application/json" \
  -d '{"Nome":"Maria Silva","Telefone":"(11)98765-4321","Data_Matricula":"2025-05-15"}'

```
- Detalhes de um Aluno:
http://localhost:5000/api/alunos/{id}

- Cadastro de Pagamento via curl:

```

curl -X POST http://localhost:5000/api/alunos/{id}/pagamentos \
  -H "Content-Type: application/json" \
  -d '{"Valor":100.00,"Tipo":"dinheiro"}'

```

## Estrutura do Projeto

```

crossx_project/
├── venv/                   # Ambiente virtual Python
├── app/                    # Pacote principal do aplicativo
│   ├── __init__.py         # Inicialização do Flask
│   ├── models.py           # Modelos: Aluno, Pagamento
│   ├── routes.py           # Rotas da interface web
│   ├── api_routes.py       # Rotas da API
│   ├── templates/          # Templates HTML
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── alunos/
│   │   │   ├── lista.html
│   │   │   ├── novo.html
│   │   │   └── detalhes.html
│   │   └── pagamentos/
│   │       └── novo.html
│   └── static/
│       └── css/
│           └── style.css
├── config.py               # Configurações do aplicativo
└── run.py                  # Início do servidor

```

## API Documentation
### Endpoints Disponíveis

| Método | Endpoint                                | Descrição                                 |
|--------|-----------------------------------------|-------------------------------------------|
| GET    | /api/                                   | Verificar status da API                   |
| GET    | /api/alunos                             | Listar todos os alunos                    |
| POST   | /api/alunos                             | Cadastrar novo aluno                      |
| GET    | /api/alunos/{id}                        | Obter detalhes de um aluno específico     |
| PUT    | /api/alunos/{id}                        | Atualizar informações de um aluno         |
| DELETE | /api/alunos/{id}                        | Excluir um aluno                          |
| POST   | /api/alunos/{id}/desligar               | Desligar um aluno                         |
| GET    | /api/alunos/{id}/pagamentos             | Listar pagamentos de um aluno             |
| POST   | /api/alunos/{id}/pagamentos             | Registrar novo pagamento para um aluno    |
| GET    | /api/pagamentos/{id}                    | Obter detalhes de um pagamento específico |
| DELETE | /api/pagamentos/{id}                    | Excluir um pagamento                      |

### Exemplo de Resposta da API

```

{
  "ID_Aluno": 1,
  "Nome": "João da Silva",
  "Endereco": "Rua das Flores, 123",
  "Cidade": "São Paulo",
  "Estado": "SP",
  "Telefone": "(11) 98765-4321",
  "Data_Matricula": "2025-05-15",
  "Data_Desligamento": null,
  "Data_Vencimento": "2025-06-15"
}

```
## Troubleshooting
### Problemas Comuns
- Erro de Porta em Uso  
**Mensagem:** "Address already in use"  
**Solução:** Encerre o processo que está utilizando a porta ou modifique a porta no run.py.

- Erro de Banco de Dados  
**Mensagem:** "No such table: aluno"  
**Solução:** Verifique se o banco foi criado. Pode ser necessário apagar crossx.db e reiniciar o app.

- Erro ao Executar o Python  
**Solução:** Verifique se o ambiente virtual está ativado e o Python está no PATH.

- Bibliotecas Faltando  
**Mensagem:** ModuleNotFoundError: No module named 'flask'  
**Solução:** Execute:

```

pip install Flask Flask-SQLAlchemy

```

**Desenvolvido como projeto acadêmico © 2025**
