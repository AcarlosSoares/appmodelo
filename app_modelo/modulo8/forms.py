from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app_modelo.modulo6.models import Professor, Aluno

ordenarporProfessor_choices=[('professor_prf.id_prf', 'Id'), ('professor_prf.nome_prf', 'Nome')]
ordenarporAluno_choices=[('aluno_aln.id_aln', 'Id'), ('aluno_aln.nome_aln', 'Nome')]
ordem_choices=[('ASC', 'Asc'), ('DESC', 'Desc')]

class ListaProfessorForm(FlaskForm):
  ordenarpor = SelectField('Ordenar Por', choices=ordenarporProfessor_choices)
  ordem = SelectField('Ordem', choices=ordem_choices)
  pesquisarpor = StringField('Filtrar Por')
  submit_enviar = SubmitField('Enviar')
  submit_limpar = SubmitField('Limpar')

class IncluiProfessorForm(FlaskForm):
  nome = StringField('Nome', validators=[DataRequired(message='Nome deve ser prenchido!'), Length(min=3, max=100, message='Nome deve ter entre 3 e 100 caracteres!')])
  submit = SubmitField('Enviar')

  def validate_nome(self, nome):
      dado = Professor.query.filter_by(nome=nome.data).first()
      if dado:
        raise ValidationError('Nome já registrado. Por favor, escolha um nome diferente.')

class AlteraProfessorForm(FlaskForm):
  nome = StringField('Nome', validators=[DataRequired(message='Nome deve ser prenchido!'), Length(min=3, max=100, message='Nome deve ter entre 3 e 100 caracteres!')])
  submit = SubmitField('Enviar')

  def validate_nome(self, nome):
      dado = Professor.query.filter_by(nome=nome.data).first()
      if dado:
        raise ValidationError('Nome já registrado. Por favor, escolha um nome diferente.')

class ListaAlunosPorProfessorForm(FlaskForm):
  ordenarpor = SelectField('Ordenar Por', choices=ordenarporAluno_choices)
  ordem = SelectField('Ordem', choices=ordem_choices)
  pesquisarpor = StringField('Filtrar Por')
  submit_enviar = SubmitField('Enviar')
  submit_limpar = SubmitField('Limpar')

class ListaAlunoForm(FlaskForm):
  ordenarpor = SelectField('Ordenar Por', choices=ordenarporAluno_choices)
  ordem = SelectField('Ordem', choices=ordem_choices)
  pesquisarpor = StringField('Filtrar Por')
  submit_enviar = SubmitField('Enviar')
  submit_limpar = SubmitField('Limpar')

class IncluiAlunoForm(FlaskForm):
  nome = StringField('Nome', validators=[DataRequired(message='Nome deve ser prenchido!'), Length(min=3, max=100, message='Nome deve ter entre 3 e 100 caracteres!')])
  submit = SubmitField('Enviar')

  def validate_nome(self, nome):
      dado = Aluno.query.filter_by(nome=nome.data).first()
      if dado:
        raise ValidationError('Nome já registrado. Por favor, escolha um nome diferente.')

class AlteraAlunoForm(FlaskForm):
  nome = StringField('Nome', validators=[DataRequired(message='Nome deve ser prenchido!'), Length(min=3, max=100, message='Nome deve ter entre 3 e 100 caracteres!')])
  submit = SubmitField('Enviar')

  def validate_nome(self, nome):
      dado = Aluno.query.filter_by(nome=nome.data).first()
      if dado:
        raise ValidationError('Nome já registrado. Por favor, escolha um nome diferente.')

