from flask import current_app
from app_modelo import db
from datetime import datetime


professor_aluno = db.Table('professor_aluno_pfa',
    db.Column('id_prf', db.Integer, db.ForeignKey('professor_prf.id_prf'), primary_key=True),
    db.Column('id_aln', db.Integer, db.ForeignKey('aluno_aln.id_aln'), primary_key=True)
    # extend_existing=True
)


class Professor(db.Model):

  __tablename__ = 'professor_prf'
  # __table_args__ = {'extend_existing': True}

  id = db.Column("id_prf", db.Integer, primary_key=True)
  nome = db.Column("nome_prf", db.String(50))
  data_criacao = db.Column("dt_criacao_prf", db.DateTime, default=datetime.utcnow)
  alunos = db.relationship('modulo6.models.Aluno', secondary=professor_aluno, backref=db.backref('professores', lazy='dynamic'))


class Aluno(db.Model):

  __tablename__ = 'aluno_aln'
  # __table_args__ = {'extend_existing': True}

  id = db.Column("id_aln", db.Integer, primary_key=True)
  nome = db.Column("nome_aln", db.String(50))
