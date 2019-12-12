# coding: utf-8

from flask import current_app
from app_modelo import db


class Empresa(db.Model):

    __tablename__ = 'tb_empresa_emp'

    id_empresa= db.Column('id_empresa', db.Integer, primary_key=True)
    ds_nomefantasia_emp= db.Column('ds_nomefantasia_emp', db.String(60), nullable=False)
    ds_razaosocial_emp= db.Column('ds_razaosocial_emp', db.String(100), nullable=False)
    ds_cnpj_emp= db.Column('ds_cnpj_emp', db.String(25), nullable=False)
    ds_cidade_emp= db.Column('ds_cidade_emp', db.String(50), nullable=False)
