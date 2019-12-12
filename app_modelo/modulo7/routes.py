from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint, make_response)
from flask_login import current_user, login_required
from sqlalchemy import desc, asc, text
from app_modelo import db
from app_modelo.modulo7.models import Pessoa, Empregado
from app_modelo.modulo7.forms import ListaPessoaEmpregadoForm, IncluiPessoaEmpregadoForm, AlteraPessoaEmpregadoForm
import os

modulo7 = Blueprint('modulo7', __name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))


@modulo7.route('/', methods=['GET'])
@login_required
def index():
  try:
    return render_template('modulo7.html', title='Modulo 7')
  except TemplateNotFound:
    abort(404)


@modulo7.route('/modulo7/acessar', methods=['GET', 'POST'])
@login_required
def acessar():

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo7.acessar'))

  form = ListaPessoaEmpregadoForm()

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
    return redirect(url_for('modulo7.acessar'))

  try:
    page = request.form.get('page', 1, type=int)
    if ordenarpor and ordem and pesquisarpor:
      order_column = text(ordenarpor + ' ' + ordem)
      filter_column = text(ordenarpor + ' LIKE ' + "'%" + pesquisarpor + "%'")
      dados = Pessoa.query.order_by(order_column).filter(filter_column).paginate(page=page, per_page=8)
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Pessoa.query.order_by(order_column).paginate(page=page, per_page=8)
    else:
      dados = Pessoa.query.paginate(page=page, per_page=8)
    return render_template('lista_pessoa.html', title='Lista de Pessoas', dados=dados, form=form)
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('users.logout'))


@modulo7.route('/modulo7/incluir', methods=['GET', 'POST'])
@login_required
def incluir():

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo7.acessar'))

  form = IncluiPessoaEmpregadoForm()

  if request.method == 'GET':
    return render_template('inclui_pessoa.html', title='Incluir Pessoa', form=form)

  if not form.validate_on_submit():
    return render_template('inclui_pessoa.html', title='Incluir Pessoa', form=form)

  if form.validate_on_submit():
    try:
      dado = Pessoa(nome=form.nome.data, datanascimento=form.datanascimento.data)
      db.session.add(dado)
      dado1 = Empregado(matricula=form.matricula.data,
        nomeguerra=form.nomeguerra.data,
        dataadmissao=form.dataadmissao.data,
        pessoa=dado)
      db.session.add(dado1)
      db.session.commit()
      flash('Registro foi incluído com sucesso!', 'success')
      return redirect(url_for('modulo7.acessar'))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo7.acessar'))


@modulo7.route("/modulo7/excluir/<int:id_data>", methods=['POST'])
@login_required
def excluir(id_data):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo7.acessar'))

  try:
    dado = Pessoa.query.get(id_data)
    if dado:
      db.session.delete(dado)
      db.session.commit()
      flash('Registro foi excluido com sucesso!', 'success')
      return redirect(url_for('modulo7.acessar'))
    else:
      flash('Falha na exclusão!', 'danger')
      return redirect(url_for('modulo7.acessar'))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo7.acessar'))


@modulo7.route('/modulo7/alterar/<int:id_data>', methods=['GET', 'POST'])
@login_required
def alterar(id_data):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo7.acessar'))

  form = AlteraPessoaEmpregadoForm()

  if request.method == 'GET':
    try:
      dado = Pessoa.query.get(id_data)
      form.nome.data = dado.nome
      form.datanascimento.data = dado.datanascimento
      form.matricula.data = dado.empregado.matricula
      form.nomeguerra.data = dado.empregado.nomeguerra
      form.dataadmissao.data = dado.empregado.dataadmissao
      return render_template('altera_pessoa.html', title='Alterar Pessoa', form=form)
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo7.acessar'))

  if not form.validate_on_submit():
    return render_template('altera_pessoa.html', title='Alterar Pessoa', form=form)

  if form.validate_on_submit():
    try:
      dado = Pessoa.query.get(id_data)
      dado.nome = form.nome.data
      dado.datanascimento = form.datanascimento.data
      dado.empregado.matricula = form.matricula.data
      dado.empregado.nomeguerra = form.nomeguerra.data
      dado.empregado.dataadmissao = form.dataadmissao.data
      db.session.commit()
      flash('Registro foi alterado com sucesso!', 'success')
      return redirect(url_for('modulo7.acessar'))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo7.acessar'))


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
      dados = Pessoa.query.order_by(order_column).filter(filter_column).all()
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Pessoa.query.order_by(order_column).all()
    else:
      dados = Pessoa.query.all()
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo7.acessar'))

  # # # PARÂMETROS DO RELATÓRIO
  titulo = 'LISTA DE PESSOAS'
  subtitulo = None
  lista = [
    ['ID', 'row.id', 50, 80],
    ['NOME', 'row.nome', 100, 300],
    ['NOME DE GUERRA', 'row.empregado.nomeguerra', 320, 440],
    ['MATRÍCULA', 'row.empregado.matricula', 460, 540]
  ]

  response = imprimir_reportlab(titulo, subtitulo, lista, dados)
  return response
