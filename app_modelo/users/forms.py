from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from app_modelo.users.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Informe seu endereço de email'),
        Email(message='Endereço do email inválido!')])
    password = PasswordField('Senha', validators=[
        DataRequired()])
    remember = BooleanField('Lembre-me')
    submit = SubmitField('Enviar')


class RegistrationForm(FlaskForm):
    username = StringField('Usuário', validators=[
        DataRequired(message='Informe o seu usuário!'),
        Length(min=2, max=20)])
    email = StringField('Email', validators=[
        DataRequired(message='Informe seu endereço de email!'),
        Email(message='Endereço do email inválido!')])
    password = PasswordField('Senha', validators=[
        DataRequired(message='Informe a sua senha!')])
    confirm_password = PasswordField('Confirme sua senha!', validators=[
        DataRequired(message='Confirme a sua senha!'),
        EqualTo('password')])
    submit = SubmitField('Enviar')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Usuário já registrado. Por favor, escolha um usuário diferente.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email já registrado. Por favor, escolha um email diferente.')


class UpdateAccountForm(FlaskForm):
    username = StringField('Usuário',validators=[
        DataRequired(message='Informe o seu usuário!'),
        Length(min=2, max=20,
        message='Usuário deve ter entre 3 e 20 caracteres!')])
    email = StringField('Email', validators=[
        DataRequired(message='Informe seu endereço de email!'),
        Email(message='Endereço do email inválido!')])
    picture = FileField('Atualize a foto da sua conta', validators=[
        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Atualizar')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Usuário já registrado. Por favor, escolha um usuário diferente.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email já registrado. Por favor, escolha um email diferente.')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(message='Informe seu endereço de email!'),
        Email(message='Endereço do email inválido!')])
    submit = SubmitField('Solicite nova senha')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Não existe uma conta registrada com este email. Voce deve primeiro se registrar.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Senha', validators=[
        DataRequired(message='Informe a sua senha!')])
    confirm_password = PasswordField('Confirme a sua senha', validators=[
        DataRequired(message='Confirme a sua senha!'),
        EqualTo('password')])
    submit = SubmitField('Enviar')
