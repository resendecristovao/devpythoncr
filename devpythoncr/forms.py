from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SearchField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from devpythoncr.models import Usuario

class FormCriarConta(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(6,20)])
    confirmacao_senha = PasswordField('Confirmação da Senha', validators=[DataRequired(), EqualTo('senha')])
    tokenaut = StringField('Token', validators=[DataRequired()])
    botao_submit_criarconta = SubmitField('Criar Conta')

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('E-mail já cadastrado. Cadastre-se com outro e-mail ou faça login')


class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    senha = PasswordField('Senha', validators=[DataRequired()])
    lembrar_dados = BooleanField('Lembrar dados')
    botao_submit_login = SubmitField('Fazer Login')

class FormBuscar(FlaskForm):
    busca = StringField('E-mail a ser procurado', validators=[DataRequired()])
    botao_submit_busca = SubmitField('Buscar')