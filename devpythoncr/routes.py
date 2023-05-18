from flask import render_template, redirect, url_for, flash, request
from devpythoncr import app, database, bcrypt
from devpythoncr.forms import FormLogin, FormCriarConta, FormBuscar
from devpythoncr.models import Usuarios, Registros
from flask_login import login_user, logout_user, current_user, login_required
import json


@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('registros'))
    else:
        return redirect(url_for('login'))

@app.route('/registros', methods=['GET', 'POST'])
@login_required
def registros():
    form_buscar = FormBuscar()
    if request.method == 'POST':
        if form_buscar.validate_on_submit() and 'botao_submit_busca' in request.form:
            registros = Registros.query.filter_by(email=form_buscar.busca.data.lower()).all()
            if registros:
                return render_template('registros.html', registros=registros, form_buscar=form_buscar)
            else:
                flash('Nenhum resultado encontrado.', 'alert-danger')
                return redirect(url_for('registros'))
        else:
            flash('Nenhum resultado encontrado.', 'alert-danger')
            return redirect(url_for('registros'))
    else:
        registros = Registros.query.all()
        return render_template('registros.html', registros=registros, form_buscar=form_buscar)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and 'botao_submit_login' in request.form:
        usuario = Usuarios.query.filter_by(email=form_login.email.data.lower()).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            return redirect(url_for('home'))
        else:
            flash('Falha no login. E-mail ou Senha incorretos.', 'alert-danger')
            return redirect(url_for('login'))
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        if form_criarconta.tokenaut.data == 'uhdfaAADF123':
            senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode("utf-8")
            usuario = Usuarios(email=form_criarconta.email.data.lower(), senha=senha_cript)
            with app.app_context():
                database.session.add(usuario)
                database.session.commit()
            flash(f'Conta criada para o e-mail: {form_criarconta.email.data}', 'alert-success')
            return redirect(url_for('home'))
        else:
            flash('Token Inválido!', 'alert-danger')
            return redirect(url_for('login'))
    return render_template('login.html', form_login=form_login, form_criarconta=form_criarconta)


@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Logout efetuado', 'alert-success')
    return redirect(url_for('login'))

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        dados = json.loads(request.data)
        if dados['status'] == 'aprovado':
            print(f"Liberar acesso do e-mail: {dados['email']}")
            print(f"Enviar mensagem de boas vindas para o e-mail: {dados['email']}")
            acao = 'Acesso liberado e e-mail de boas vindas enviado'
        elif dados['status'] == 'recusado':
            print(f"Enviar mensagem de pagamento recusado para o e-mail: {dados['email']}")
            acao = 'E-mail de pagamento recusado enviado'
        elif dados['status'] == 'reembolsado':
            print(f"Remover acesso do e-mail: {dados['email']}")
            acao = 'Acesso removido'
        else:
            acao = ''
        with app.app_context():
            registro = Registros(nome=dados['nome'], email=dados['email'].lower(), status=dados['status'], valor=dados['valor'],
                                  forma_pagamento=dados['forma_pagamento'], parcelas=dados['parcelas'], acao=acao)
            database.session.add(registro)
            database.session.commit()
        return '200'
    else:
        return '404'
