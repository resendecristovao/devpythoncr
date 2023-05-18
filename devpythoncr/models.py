from devpythoncr import database, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_usuario(id_usuario):
    return Usuario.query.get(int(id_usuario))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)


class Registros(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    data = database.Column(database.DateTime, nullable=False, default=datetime.utcnow)
    nome = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False)
    status = database.Column(database.String, nullable=False)
    valor = database.Column(database.Float, nullable=False)
    forma_pagamento = database.Column(database.String, nullable=False)
    parcelas = database.Column(database.Integer, nullable=False)
