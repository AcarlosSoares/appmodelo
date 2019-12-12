from flask import current_app
from app_modelo import db


class Modelo(db.Model):

    __tablename__ = 'modelo_mod'
    __table_args__ = {'extend_existing': True}


    id = db.Column("id_modelo", db.Integer, primary_key=True)
    sigla = db.Column("ds_sigla_mod", db.String(45), nullable=False)
    nome = db.Column("ds_nome_mod", db.String(100), nullable=False)

    def __repr__(self):
        return f"Modelo('{self.sigla}', '{self.nome}')"

