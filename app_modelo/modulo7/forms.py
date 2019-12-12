from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields.html5 import DateField
from app_modelo.modulo7.models import Pessoa, Empregado


ordenarpor_choices=[('pessoa_pes.id_pes', 'Id'), ('pessoa_pes.nome_pes', 'Nome'), \
 ('empregado_emp_1.nm_guerra_emp', 'Nome de Guerra'), ('empregado_emp_1.matricula_emp', 'Matrícula')]
ordem_choices=[('ASC', 'Asc'), ('DESC', 'Desc')]


class ListaPessoaEmpregadoForm(FlaskForm):
  ordenarpor = SelectField('Ordenar Por', choices=ordenarpor_choices)
  ordem = SelectField('Ordem', choices=ordem_choices)
  pesquisarpor = StringField('Filtrar Por')
  submit_enviar = SubmitField('Enviar')
  submit_limpar = SubmitField('Limpar')


class IncluiPessoaEmpregadoForm(FlaskForm):
  nome = StringField('Nome', validators=[DataRequired(message='Nome deve ser prenchido!'),
   Length(min=3, max=80, message='Nome deve ter entre 3 e 80 caracteres!')])
  datanascimento = DateField('Data de Nascimento', validators=[DataRequired(message='Data deve ser prenchida!')],
   format=('%Y-%m-%d'))
  matricula = StringField('Matrícula', validators=[DataRequired(message='Nome deve ser prenchido!'),
   Length(min=5, max=11, message='Nome deve ter entre 5 e 11 caracteres!')])
  nomeguerra = StringField('Nome de Guerra', validators=[DataRequired(message='Nome deve ser prenchido!'),
   Length(min=3, max=20, message='Nome deve ter entre 3 e 20 caracteres!')])
  dataadmissao = DateField('Data de Admissão', validators=[DataRequired(message='Data deve ser prenchida!')],
   format=('%Y-%m-%d'))
  submit = SubmitField('Enviar')

  def validate_nome(self, nome):
      dado = Pessoa.query.filter_by(nome=nome.data).first()
      if dado:
        raise ValidationError('Nome já registrado. Por favor, escolha um nome diferente.')


class AlteraPessoaEmpregadoForm(FlaskForm):
  nome = StringField('Nome', validators=[DataRequired(message='Nome deve ser prenchido!'),
   Length(min=3, max=80, message='Nome deve ter entre 3 e 80 caracteres!')])
  datanascimento = DateField('Data de Nascimento', validators=[DataRequired(message='Data deve ser prenchida!')],
   format=('%Y-%m-%d'))
  matricula = StringField('Matrícula', validators=[DataRequired(message='Nome deve ser prenchido!'),
   Length(min=5, max=11, message='Nome deve ter entre 5 e 11 caracteres!')])
  nomeguerra = StringField('Nome de Guerra', validators=[DataRequired(message='Nome deve ser prenchido!'),
   Length(min=3, max=20, message='Nome deve ter entre 3 e 20 caracteres!')])
  dataadmissao = DateField('Data de Admissão', validators=[DataRequired(message='Data deve ser prenchida!')],
   format=('%Y-%m-%d'))
  submit = SubmitField('Enviar')

  def validate_nome(self, nome):
      dado = Pessoa.query.filter_by(nome=nome.data).first()
      if dado:
        raise ValidationError('Nome já registrado. Por favor, escolha um nome diferente.')
