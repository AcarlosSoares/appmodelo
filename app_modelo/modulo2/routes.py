from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint, make_response)
from flask_login import current_user, login_required
from sqlalchemy import desc, asc, text
from app_modelo import db
from app_modelo.modulo2.models import Modelo
from app_modelo.modulo2.forms import ListaForm, IncluiForm, AlteraForm
import os

modulo2 = Blueprint('modulo2', __name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))


@modulo2.route('/modulo2/acessar', methods=['GET', 'POST'])
@login_required
def acessar():

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo2.acessar'))

  form = ListaForm()

  ordenarpor = request.form.get('ordenarpor')
  ordem = request.form.get('ordem')
  pesquisarpor = request.form.get('pesquisarpor')


  try:
    imprimir = request.form.get('imprimir')
    if imprimir:
      response = imprimir1()
      return response
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('conta.logout'))

  limpar = request.form.get('submit_limpar')
  if limpar:
    form.ordenarpor.data = 'modelo_mod.id_modelo'
    form.ordenarpor.data = 'ASC'
    form.ordenarpor.data = None
    return redirect(url_for('modulo2.acessar'))

  try:
    page = request.form.get('page', 1, type=int)
    if ordenarpor and ordem and pesquisarpor:
      order_column = text(ordenarpor + ' ' + ordem)
      filter_column = text(ordenarpor + ' LIKE ' + "'%" + pesquisarpor + "%'")
      dados = Modelo.query.order_by(order_column).filter(filter_column).paginate(page=page, per_page=8)
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Modelo.query.order_by(order_column).paginate(page=page, per_page=8)
    else:
      dados = Modelo.query.paginate(page=page, per_page=8)
    return render_template('lista.html', title='Lista de Modelos', dados=dados, form=form)
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('users.logout'))


@modulo2.route('/modulo2/incluir', methods=['GET', 'POST'])
@login_required
def incluir():

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo2.acessar'))

  form = IncluiForm()

  if request.method == 'GET':
    return render_template('inclui.html', title='Incluir Modelo', form=form)

  if not form.validate_on_submit():
    return render_template('inclui.html', title='Incluir Modelo', form=form)

  if form.validate_on_submit():
    try:
      dado = Modelo(sigla=form.sigla.data, nome=form.nome.data)
      db.session.add(dado)
      db.session.commit()
      flash('Registro foi incluído com sucesso!', 'success')
      return redirect(url_for('modulo2.acessar'))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo2.acessar'))


@modulo2.route("/modulo2/excluir/<int:id_data>", methods=['POST'])
@login_required
def excluir(id_data):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo2.acessar'))

  try:
    dado = Modelo.query.get(id_data)
    if dado:
      db.session.delete(dado)
      db.session.commit()
      flash('Registro foi excluido com sucesso!', 'success')
      return redirect(url_for('modulo2.acessar'))
    else:
      flash('Falha na exclusão!', 'danger')
      return redirect(url_for('modulo2.acessar'))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo2.acessar'))


@modulo2.route('/modulo2/alterar/<int:id_data>', methods=['GET', 'POST'])
@login_required
def alterar(id_data):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo2.acessar'))

  form = AlteraForm()

  if request.method == 'GET':
    try:
      dado = Modelo.query.get(id_data)
      form.seq.data = id_data
      form.sigla.data = dado.sigla
      form.nome.data = dado.nome
      return render_template('altera.html', title='Alterar Modelo', form=form)
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo2.acessar'))

  if not form.validate_on_submit():
    return render_template('altera.html', title='Alterar Modelo', form=form)

  if form.validate_on_submit():
    try:
      dado = Modelo.query.get(id_data)
      dado.sigla = form.sigla.data
      dado.nome = form.nome.data
      db.session.commit()
      flash('Registro foi alterado com sucesso!', 'success')
      return redirect(url_for('modulo2.acessar'))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo2.acessar'))


def imprimir1():

  from app_modelo.principal.relatorios import imprimir_reportlab

  ordenarpor = request.form.get('ordenarpor')
  ordem = request.form.get('ordem')
  pesquisarpor = request.form.get('pesquisarpor')

  # LÊ BASE DE DADOS
  try:
    if ordenarpor and ordem and pesquisarpor:
      order_column = text(ordenarpor + ' ' + ordem)
      filter_column = text(ordenarpor + ' LIKE ' + "'%" + pesquisarpor + "%'")
      dados = Modelo.query.order_by(order_column).filter(filter_column).all()
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Modelo.query.order_by(order_column).all()
    else:
      dados = Modelo.query.all()
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo2.acessar'))

  # # # PARÂMETROS DO RELATÓRIO
  titulo = 'LISTA DE MODELOS'
  subtitulo = None
  lista = [
    ['ID', 'row.id', 50, 80],
    ['SIGLA', 'row.sigla', 100, 180],
    ['NOME', 'row.nome', 200, 400]
  ]

  response = imprimir_reportlab(titulo, subtitulo, lista, dados)
  return response
