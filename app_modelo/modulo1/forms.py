from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app_modelo.modulo1.models import Modelo

def my_length_check(form, field):
  if len(field.data) > 2 and len(field.data) < 45:
    raise ValidationError('Campo deve ter entre 3 e 50 caracteres!')

# https://wtforms.readthedocs.io/en/stable/validators.html
def length(min=-1, max=-1):
    message = 'Must be between %d and %d characters long.' % (min, max)
    def _length(form, field):
        l = field.data and len(field.data) or 0
        if l < min or max != -1 and l > max:
            raise ValidationError(message)
    return _length

def modelo_check(form, field):
  modelo = Modelo.query.filter_by(sigla=sigla.data).first()
  if modelo:
      raise ValidationError('Sigla já registrada. Por favor, escolha uma sigla diferente.')

class ListaModeloForm(FlaskForm):
  sigla = StringField('Sigla', validators=[DataRequired(message='Sigla deve ser prenchido!'),
   Length(min=2, max=45, message='Sigla deve ter entre 3 e 50 caracteres!')])
  nome = StringField('Nome', validators=[DataRequired(message='Nome deve ser prenchido!'), Length(min=2, max=100, message='Nome deve ter entre 3 e 100 caracteres!')])
  submit = SubmitField('Enviar')

  def validate_sigla(self, sigla):
      modelo = Modelo.query.filter_by(sigla=sigla.data).first()
      if modelo:
          raise ValidationError('Sigla já registrada. Por favor, escolha uma sigla diferente.')

  # def validate_nome(self, nome):
  #     modelo = Modelo.query.filter_by(nome=nome.data).first()
  #     if modelo:
  #       raise ValidationError('Nome já registrado. Por favor, escolha um nome diferente.')
