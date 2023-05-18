from flask import render_template, redirect, url_for, flash, request
from devpythoncr import app, database, bcrypt
from devpythoncr.forms import FormLogin, FormCriarConta, FormBuscar
from devpythoncr.models import Usuario, Registros
from flask_login import login_user, logout_user, current_user, login_required


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
            registros = Registros.query.filter_by(email=form_buscar.busca.data).all()
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
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(f'Login feito com sucesso no e-mail: {form_login.email.data}', 'alert-success')
            return redirect(url_for('home'))
        else:
            flash('Falha no login. E-mail ou Senha incorretos.', 'alert-danger')
            return redirect(url_for('login'))
    if form_criarconta.validate_on_submit() and 'botao_submit_criarconta' in request.form:
        if form_criarconta.tokenaut.data == 'uhdfaAADF123':
            senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data)
            usuario = Usuario(email=form_criarconta.email.data, senha=senha_cript)
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