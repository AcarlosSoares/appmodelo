from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, DateField, TextAreaField, RadioField,  SelectField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from app_modelo.modulo5.models import Detalhe, Mestre
from app_modelo.modulo2.models import Modelo

ordenarporMestre_choices=[('mestre_mst.id_mst', 'Id'), ('mestre_mst.ds_nome_mst', 'Nome'), \
 ('mestre_mst.ds_estadocivil_mst', 'Estado Civil')]
ordenarporDetalhe_choices=[('detalhe_dtl.id_dtl', 'Id'), ('detalhe_dtl.ds_nome_dtl', 'Nome'), \
 ('detalhe_dtl.ds_cidade_dtl', 'Cidade')]
ordem_choices=[('ASC', 'Asc'), ('DESC', 'Desc')]

estadocivil_choices=[('1', 'Solteiro'), ('2', 'Casado'), ('3', 'Separado'), ('4', 'Divorciado')]
sexo_choices=[('M', 'Masculino'), ('F', 'Feminino')]

class ListaMestreForm(FlaskForm):
  ordenarpor = SelectField('Ordenar Por', choices=ordenarporMestre_choices)
  ordem = SelectField('Ordem', choices=ordem_choices)
  pesquisarpor = StringField('Filtrar Por')
  submit_enviar = SubmitField('Enviar')
  submit_limpar = SubmitField('Limpar')


class AlteraMestreForm(FlaskForm):
  nome = StringField('Nome', validators=[DataRequired(message='Nome deve ser prenchido!'), Length(min=3, max=80, message='Nome deve ter entre 3 e 80 caracteres!')])
  sexo = RadioField(default='M', choices=sexo_choices)
  estadocivil = SelectField('Estado Civil', choices=estadocivil_choices)
  # estadocivil = SelectField('Estado Civil')
  datanascimento = DateField('Data de Nascimento', validators=[DataRequired(message='Data deve ser prenchida!')], format=('%Y-%m-%d'))
  situacao = BooleanField('Ativo')
  submit = SubmitField('Enviar')

  # def __init__(self):
  #   super(AlteraMestreForm, self).__init__()
  #   self.estadocivil.choices = [(k.id, k.sigla) for k in Modelo.query.all()]

class IncluiMestreForm(FlaskForm):
  nome = StringField('Nome', validators=[DataRequired(message='Nome deve ser prenchido!'), Length(min=3, max=80, message='Nome deve ter entre 3 e 80 caracteres!')])
  sexo = RadioField(default='M', choices=sexo_choices)
  estadocivil = SelectField('Estado Civil', choices=estadocivil_choices)
  # estadocivil = SelectField('Estado Civil')
  datanascimento = DateField('Data de Nascimento', validators=[DataRequired(message='Data deve ser prenchida!')], format=('%Y-%m-%d'))
  situacao = BooleanField('Ativo')
  submit = SubmitField('Enviar')

  # def __init__(self):
  #   super(IncluiMestreForm, self).__init__()
  #   self.estadocivil.choices = [(k.id, k.sigla) for k in Modelo.query.all()]

# https://stackoverflow.com/questions/33832940/flask-how-to-populate-select-field-in-wtf-form-when-database-files-is-separate
# https://kyle.marek-spartz.org/posts/2014-04-04-setting-wtforms-selection-fields-dynamically.html

class ListaDetalheForm(FlaskForm):
  ordenarpor = SelectField('Ordenar Por', choices=ordenarporDetalhe_choices)
  ordem = SelectField('Ordem', choices=ordem_choices)
  pesquisarpor = StringField('Filtrar Por')
  submit_enviar = SubmitField('Enviar')
  submit_limpar = SubmitField('Limpar')


class AlteraDetalheForm(FlaskForm):
  nome = StringField('Nome', validators=[DataRequired(message='Deve ser prenchido!'),
    Length(min=3, max=60, message='Deve ter entre 3 e 60 caracteres!')])
  endereco = TextAreaField('Endereço', validators=[DataRequired(message='Deve ser prenchido!')])
  bairro = StringField('Bairro', validators=[DataRequired(message='Deve ser prenchido!'),
    Length(min=3, max=30, message='Deve ter entre 3 e 30 caracteres!')])
  cidade = StringField('Cidade', validators=[DataRequired(message='Deve ser prenchido!'),
    Length(min=3, max=30, message='Deve ter entre 3 e 30 caracteres!')])
  telefone = StringField('Telefone', validators=[DataRequired(message='Deve ser prenchido!'),
    Length(min=8, max=15, message='Deve ter entre 8 e 15 caracteres!')])
  submit = SubmitField('Enviar')


class AlteraDetalheForm2(FlaskForm):
  mestre = SelectField('Mestre', coerce=int)
  # mestre = SelectField('Mestre')
  nome = StringField('Nome', validators=[DataRequired(message='Deve ser prenchido!'),
    Length(min=3, max=60, message='Deve ter entre 3 e 60 caracteres!')])
  endereco = TextAreaField('Endereço', validators=[DataRequired(message='Deve ser prenchido!')])
  bairro = StringField('Bairro', validators=[DataRequired(message='Deve ser prenchido!'),
    Length(min=3, max=30, message='Deve ter entre 3 e 30 caracteres!')])
  cidade = StringField('Cidade', validators=[DataRequired(message='Deve ser prenchido!'),
    Length(min=3, max=30, message='Deve ter entre 3 e 30 caracteres!')])
  telefone = StringField('Telefone', validators=[DataRequired(message='Deve ser prenchido!'),
    Length(min=8, max=15, message='Deve ter entre 8 e 15 caracteres!')])
  submit = SubmitField('Enviar')

  def __init__(self):
    super(AlteraDetalheForm2, self).__init__()
    self.mestre.choices = [(k.id, k.nome) for k in Mestre.query.all()]


class IncluiDetalheForm(FlaskForm):
  nome = StringField('Nome', validators=[DataRequired(message='Deve ser prenchido!'),
    Length(min=3, max=60, message='Deve ter entre 3 e 60 caracteres!')])
  endereco = TextAreaField('Endereço', validators=[DataRequired(message='Deve ser prenchido!')])
  bairro = StringField('Bairro', validators=[DataRequired(message='Deve ser prenchido!'),
    Length(min=3, max=30, message='Deve ter entre 3 e 30 caracteres!')])
  cidade = StringField('Cidade', validators=[DataRequired(message='Deve ser prenchido!'),
    Length(min=3, max=30, message='Deve ter entre 3 e 30 caracteres!')])
  telefone = StringField('Telefone', validators=[DataRequired(message='Deve ser prenchido!'),
    Length(min=8, max=15, message='Deve ter entre 8 e 15 caracteres!')])
  submit = SubmitField('Enviar')


class IncluiDetalheForm2(FlaskForm):
  mestre = SelectField('Mestre', coerce=int)
  nome = StringField('Nome', validators=[DataRequired(message='Deve ser prenchido!'),
    Length(min=3, max=60, message='Deve ter entre 3 e 60 caracteres!')])
  endereco = TextAreaField('Endereço', validators=[DataRequired(message='Deve ser prenchido!')])
  bairro = StringField('Bairro', validators=[DataRequired(message='Deve ser prenchido!'),
    Length(min=3, max=30, message='Deve ter entre 3 e 30 caracteres!')])
  cidade = StringField('Cidade', validators=[DataRequired(message='Deve ser prenchido!'),
    Length(min=3, max=30, message='Deve ter entre 3 e 30 caracteres!')])
  telefone = StringField('Telefone', validators=[DataRequired(message='Deve ser prenchido!'),
    Length(min=8, max=15, message='Deve ter entre 8 e 15 caracteres!')])
  submit = SubmitField('Enviar')

  def __init__(self):
    super(IncluiDetalheForm2, self).__init__()
    self.mestre.choices = [(k.id, k.nome) for k in Mestre.query.all()]

