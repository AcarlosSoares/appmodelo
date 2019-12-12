from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property
from app_modelo import db


class Mestre(db.Model):

  # __table_args__ = {'schema': 'db_projeto_modelo'}
  __tablename__ = 'mestre_mst'

  id = db.Column("id_mst", db.Integer, primary_key=True)
  nome = db.Column("ds_nome_mst", db.String(100), nullable=False)
  sexo = db.Column("ds_sexo_mst", db.String(1), nullable=False)
  estadocivil = db.Column("ds_estadocivil_mst", db.String(1), nullable=False)
  datanascimento = db.Column("dt_nascimento_mst", db.DateTime, nullable=False)
  situacao = db.Column("lg_situacao_mst", db.Boolean)
  detalhes = db.relationship('Detalhe', backref='mestre')

  @hybrid_property
  def def_estadocivil(self):
    if self.estadocivil == '1': return 'Solteiro'
    elif self.estadocivil == '2': return 'Casado'
    elif self.estadocivil == '3': return 'Separado'
    elif self.estadocivil == '4': return 'Divorciado'
    else: return 'Desconhecido'

  @hybrid_property
  def def_sexo(self):
    if self.sexo == 'M': return 'Masculino'
    elif self.sexo == 'F': return 'Feminino'
    else: return 'Desconhecido'


class Detalhe(db.Model):

  # __table_args__ = {'schema': 'db_projeto_modelo'}
  __tablename__ = 'detalhe_dtl'

  id = db.Column("id_dtl", db.Integer, primary_key=True)
  nome = db.Column("ds_nome_dtl", db.String(60), nullable=False)
  endereco = db.Column("ds_endereco_dtl", db.String(200), nullable=False)
  bairro = db.Column("ds_bairro_dtl", db.String(30), nullable=False)
  cidade = db.Column("ds_cidade_dtl", db.String(30), nullable=False)
  telefone = db.Column("ds_telefone_dtl", db.String(15), nullable=False)
  mestre_id = db.Column("mestre_id", db.Integer, db.ForeignKey('mestre_mst.id_mst'))
