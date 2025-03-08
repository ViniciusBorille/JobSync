from flask_sqlalchemy import SQLAlchemy
from flask import Flask

# Inicializando o Flask
app = Flask(__name__)

# Configuração do banco de dados (substituir pelo seu banco)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/jobsync_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializando o SQLAlchemy
db = SQLAlchemy(app)

# Definição da classe Curriculo
class Curriculo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=False)
    cargo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    habilidades = db.Column(db.Text, nullable=False)
    formacao = db.Column(db.Text, nullable=True)

# Criando as tabelas no banco de dados
with app.app_context():
    db.create_all()
