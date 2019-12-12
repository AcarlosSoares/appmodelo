# coding: utf-8

from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint, make_response)
from flask_login import current_user, login_required
from sqlalchemy import desc, asc, text
from app_modelo import db
from app_modelo.tb_empresa_emp.models import Empresa
from app_modelo.tb_empresa_emp.forms import ListaForm, IncluiForm, AlteraForm
import os

tb_empresa_emp = Blueprint('tb_empresa_emp', __name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))


@tb_empresa_emp.route('/tb_empresa_emp/acessar', methods=['GET', 'POST'])
@login_required
def tb_empresa_emp_acessar():

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('tb_empresa_emp.tb_empresa_emp_acessar'))

  form = ListaForm()

  ordenarpor = request.form.get('ordenarpor')
  ordem = request.form.get('ordem')
  pesquisarpor = request.form.get('pesquisarpor')
  imprimir = request.form.get('imprimir')

  if imprimir:
    response = tb_empresa_emp_imprimir()
    return response

  limpar = request.form.get('submit_limpar')
  if limpar:
    form.ordenarpor.data = 'tb_empresa_emp.id_empresa'
    form.ordenarpor.data = 'ASC'
    form.ordenarpor.data = None
    return redirect(url_for('tb_empresa_emp.tb_empresa_emp_acessar'))

  try:
    page = request.form.get('page', 1, type=int)
    if ordenarpor and ordem and pesquisarpor:
      order_column = text(ordenarpor + ' ' + ordem)
      filter_column = text(ordenarpor + ' LIKE ' + "'%" + pesquisarpor + "%'")
      dados = Empresa.query.order_by(order_column).filter(filter_column).paginate(page=page, per_page=8)
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Empresa.query.order_by(order_column).paginate(page=page, per_page=8)
    else:
      dados = Empresa.query.paginate(page=page, per_page=8)
    return render_template('tb_empresa_emp_lista.html', title='Lista de Empresa', dados=dados, form=form)
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('users.logout'))


@tb_empresa_emp.route('/tb_empresa_emp/incluir', methods=['GET', 'POST'])
@login_required
def tb_empresa_emp_incluir():

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('tb_empresa_emp.tb_empresa_emp_acessar'))

  form = IncluiForm()

  if request.method == 'GET':
    return render_template('tb_empresa_emp_inclui.html', title='Incluir Empresa', form=form)

  if not form.validate_on_submit():
    flash('Formulário não validado!', 'info')
    return render_template('tb_empresa_emp_inclui.html', title='Incluir Empresa', form=form)

  if form.validate_on_submit():
    try:
      dado = Empresa(ds_nomefantasia_emp=form.ds_nomefantasia_emp.data, ds_razaosocial_emp=form.ds_razaosocial_emp.data, ds_cnpj_emp=form.ds_cnpj_emp.data, ds_cidade_emp=form.ds_cidade_emp.data)
      db.session.add(dado)
      db.session.commit()
      flash('Registro foi incluído com sucesso!', 'success')
      return redirect(url_for('tb_empresa_emp.tb_empresa_emp_acessar'))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('tb_empresa_emp.tb_empresa_emp_acessar'))


@tb_empresa_emp.route("/tb_empresa_emp/excluir/<int:id_data>", methods=['POST'])
@login_required
def tb_empresa_emp_excluir(id_data):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('tb_empresa_emp.tb_empresa_emp_acessar'))

  try:
    dado = Empresa.query.get(id_data)
    if dado:
      db.session.delete(dado)
      db.session.commit()
      flash('Registro foi excluido com sucesso!', 'success')
      return redirect(url_for('tb_empresa_emp.tb_empresa_emp_acessar'))
    else:
      flash('Falha na exclusão!', 'danger')
      return redirect(url_for('tb_empresa_emp.tb_empresa_emp_acessar'))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('tb_empresa_emp.tb_empresa_emp_acessar'))


@tb_empresa_emp.route('/tb_empresa_emp/alterar/<int:id_data>', methods=['GET', 'POST'])
@login_required
def tb_empresa_emp_alterar(id_data):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('tb_empresa_emp.tb_empresa_emp_acessar'))

  form = AlteraForm()

  if request.method == 'GET':
    try:
      dado = Empresa.query.get(id_data)
      form.ds_nomefantasia_emp.data = dado.ds_nomefantasia_emp
      form.ds_razaosocial_emp.data = dado.ds_razaosocial_emp
      form.ds_cnpj_emp.data = dado.ds_cnpj_emp
      form.ds_cidade_emp.data = dado.ds_cidade_emp
      return render_template('tb_empresa_emp_altera.html', title='Alterar Empresa', form=form)
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('tb_empresa_emp.tb_empresa_emp_acessar'))

  if not form.validate_on_submit():
    flash('Formulário não validado!', 'info')
    return render_template('tb_empresa_emp_altera.html', title='Alterar Empresa', form=form)

  if form.validate_on_submit():
    try:
      dado = Empresa.query.get(id_data)
      dado.ds_nomefantasia_emp = form.ds_nomefantasia_emp.data
      dado.ds_razaosocial_emp = form.ds_razaosocial_emp.data
      dado.ds_cnpj_emp = form.ds_cnpj_emp.data
      dado.ds_cidade_emp = form.ds_cidade_emp.data
      db.session.commit()
      flash('Registro foi alterado com sucesso!', 'success')
      return redirect(url_for('tb_empresa_emp.tb_empresa_emp_acessar'))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('tb_empresa_emp.tb_empresa_emp_acessar'))


def tb_empresa_emp_imprimir():

  from app_modelo.principal.relatorios import imprimir_reportlab

  ordenarpor = request.form.get('ordenarpor')
  ordem = request.form.get('ordem')
  pesquisarpor = request.form.get('pesquisarpor')

  # LÊ BASE DE DADOS
  try:
    if ordenarpor and ordem and pesquisarpor:
      order_column = text(ordenarpor + ' ' + ordem)
      filter_column = text(ordenarpor + ' LIKE ' + "'%" + pesquisarpor + "%'")
      dados = Empresa.query.order_by(order_column).filter(filter_column).all()
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Empresa.query.order_by(order_column).all()
    else:
      dados = Empresa.query.all()
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('tb_empresa_emp.tb_empresa_emp_acessar'))

  # # # PARÂMETROS DO RELATÓRIO
  titulo = 'LISTA DE Empresa'.upper()
  subtitulo = None
  lista = [
    ['SEQ', 'row.id_empresa', 50, 80],
    ['NOME FANTASIA', 'row.ds_nomefantasia_emp', 100, 250],
    ['RAZÃ£O SOCIAL', 'row.ds_razaosocial_emp', 270, 570]
  ]

  response = imprimir_reportlab(titulo, subtitulo, lista, dados)
  return response
