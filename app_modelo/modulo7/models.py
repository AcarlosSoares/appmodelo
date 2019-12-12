from flask import current_app
from app_modelo import db
from datetime import datetime


class Pessoa(db.Model):
  __tablename__ = 'pessoa_pes'
  id = db.Column('id_pes', db.Integer, primary_key=True)
  nome = db.Column('nome_pes', db.String(80))
  datanascimento = db.Column('dt_nascimento_pes', db.DateTime, default=datetime.utcnow)
  empregado = db.relationship('Empregado', backref='pessoa', uselist=False, lazy='joined')


class Empregado(db.Model):
  __tablename__ = 'empregado_emp'
  id = db.Column('id_emp', db.Integer, primary_key=True)
  matricula = db.Column('matricula_emp', db.String(20))
  nomeguerra = db.Column('nm_guerra_emp', db.String(20))
  dataadmissao = db.Column('dt_admissao_emp', db.DateTime, default=datetime.utcnow)
  pessoa_id = db.Column(db.Integer, db.ForeignKey('pessoa_pes.id_pes'), unique=True)
