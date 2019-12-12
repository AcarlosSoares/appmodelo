from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from sqlalchemy import desc, asc, text
from app_modelo import db
from app_modelo.modulo5.models import Mestre, Detalhe
from app_modelo.modulo5.forms import ListaMestreForm, IncluiMestreForm, AlteraMestreForm, \
 ListaDetalheForm, IncluiDetalheForm, AlteraDetalheForm, IncluiDetalheForm2, AlteraDetalheForm2
import os

modulo5 = Blueprint('modulo5', __name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))


@modulo5.route('/', methods=['GET'])
@login_required
def index():
    try:
        return render_template('modulo5.html', title='Modulo 5')
    except TemplateNotFound:
        abort(404)

# * * * MESTRE * * *
@modulo5.route('/modulo5/acessarMestre', methods=['GET', 'POST'])
@login_required
def acessarMestre():

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'warning')
    return redirect(url_for('modulo5.acessarMestre'))

  form = ListaMestreForm()

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
    form.ordenarpor.data = 'mestre_mst.id_mst'
    form.ordenarpor.data = 'ASC'
    form.ordenarpor.data = None
    return redirect(url_for('modulo5.acessarMestre'))

  try:
    page = request.form.get('page', 1, type=int)
    if ordenarpor and ordem and pesquisarpor:
      order_column = text(ordenarpor + ' ' + ordem)
      filter_column = text(ordenarpor + ' LIKE ' + "'%" + pesquisarpor + "%'")
      dados = Mestre.query.order_by(order_column).filter(filter_column).paginate(page=page, per_page=8)
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Mestre.query.order_by(order_column).paginate(page=page, per_page=8)
    else:
      dados = Mestre.query.paginate(page=page, per_page=8)
    return render_template('lista_mestre.html', title='Lista de Mestres', dados=dados, form=form)
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('users.logout'))


@modulo5.route('/modulo5/incluirMestre', methods=['GET', 'POST'])
@login_required
def incluirMestre():

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'warning')
    return redirect(url_for('modulo5.acessarMestre'))

  form = IncluiMestreForm()

  if request.method == 'GET':
    return render_template('inclui_mestre.html', title='Incluir Mestre', form=form)

  if not form.validate_on_submit():
    flash('Falha no aplicativo!' , 'danger')
    return render_template('inclui_mestre.html', title='Incluir Mestre', form=form)

  if form.validate_on_submit():
    try:
      dado = Mestre(nome=form.nome.data, sexo=form.sexo.data, datanascimento=form.datanascimento.data,
       estadocivil= form.estadocivil.data, situacao=form.situacao.data)
      db.session.add(dado)
      db.session.commit()
      flash('Registro foi incluído com sucesso!', 'success')
      return redirect(url_for('modulo5.acessarMestre'))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo5.acessarMestre'))


@modulo5.route("/modulo5/excluirMestre/<int:id_data>", methods=['POST'])
@login_required
def excluirMestre(id_data):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'warning')
    return redirect(url_for('modulo5.acessarMestre'))

  try:
    dado = Mestre.query.get(id_data)
    if dado:
      db.session.delete(dado)
      db.session.commit()
      flash('Registro foi excluido com sucesso!', 'success')
      return redirect(url_for('modulo5.acessarMestre'))
    else:
      flash('Falha na exclusão!', 'danger')
      return redirect(url_for('modulo5.acessarMestre'))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo5.acessarMestre'))


@modulo5.route('/modulo5/alterarMestre/<int:id_data>', methods=['GET', 'POST'])
@login_required
def alterarMestre(id_data):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'warning')
    return redirect(url_for('modulo5.acessarMestre'))

  form = AlteraMestreForm()

  if request.method == 'GET':
    try:
      dado = Mestre.query.get(id_data)
      form.nome.data = dado.nome
      form.sexo.data = dado.sexo
      form.datanascimento.data = dado.datanascimento
      form.estadocivil.process_data(dado.estadocivil)
      form.situacao.data = dado.situacao
      return render_template('altera_mestre.html', title='Alterar Mestre', form=form)
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo5.acessarMestre'))

  if not form.validate_on_submit():
    flash('Falha no aplicativo!' , 'danger')
    return render_template('altera_mestre.html', title='Alterar Mestre', form=form)

  if form.validate_on_submit():
    try:
      dado = Mestre.query.get(id_data)
      dado.nome = form.nome.data
      dado.sexo = form.sexo.data
      dado.datanascimento = form.datanascimento.data
      dado.estadocivil = form.estadocivil.data
      dado.situacao = form.situacao.data
      db.session.commit()
      flash('Registro foi alterado com sucesso!', 'success')
      return redirect(url_for('modulo5.acessarMestre'))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo5.acessarMestre'))


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
      dados = Mestre.query.order_by(order_column).filter(filter_column).all()
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Mestre.query.order_by(order_column).all()
    else:
      dados = Mestre.query.all()
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo5.acessarMestre'))

  # # # PARÂMETROS DO RELATÓRIO
  titulo = 'LISTA DE MESTRES'
  subtitulo = None
  lista = [
    ['ID', 'row.id', 50, 80],
    ['NOME', 'row.nome', 100, 300],
    ['ESTADO CIVIL', 'row.def_estadocivil', 320, 400]
  ]

  response = imprimir_reportlab(titulo, subtitulo, lista, dados)
  return response


# * * * DETALHE * * *
# @modulo5.route('/modulo5/acessarDetalhe', methods=['GET'])
# @login_required
# def acessarDetalhe():

#   if not current_user.is_authenticated:
#     flash('Usuário não autorizado!', 'warning')
#     return redirect(url_for('modulo5.acessarDetalhe'))

#   form = ListaDetalheForm()

#   try:
#     page = request.args.get('page', 1, type=int)
#     dados = Detalhe.query.paginate(page=page, per_page=8)
#     return render_template('lista_detalhe.html', title='Lista de Detalhes', dados=dados, form=form)
#   except Exception as e:
#     flash('Falha no aplicativo! ' + str(e), 'danger')
#     return redirect(url_for('users.logout'))


@modulo5.route('/modulo5/acessarDetalhe/<int:id_mst>/<string:nome_mst>', methods=['GET', 'POST'])
@login_required
def acessarDetalhe(id_mst, nome_mst):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'warning')
    return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))

  form = ListaDetalheForm()

  ordenarpor = request.form.get('ordenarpor')
  ordem = request.form.get('ordem')
  pesquisarpor = request.form.get('pesquisarpor')

  try:
    imprimir = request.form.get('imprimir')
    if imprimir:
      response = imprimir2(id_mst, nome_mst)
      return response
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('conta.logout'))

  limpar = request.form.get('submit_limpar')
  if limpar:
    form.ordenarpor.data = 'detalhe_dtl.id_dtl'
    form.ordenarpor.data = 'ASC'
    form.ordenarpor.data = None
    return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))

  try:
    page = request.form.get('page', 1, type=int)
    if ordenarpor and ordem and pesquisarpor:
      order_column = text(ordenarpor + ' ' + ordem)
      filter_column = text(ordenarpor + ' LIKE ' + "'%" + pesquisarpor + "%'")
      dados = Detalhe.query.order_by(order_column).filter(filter_column).paginate(page=page, per_page=8)
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Detalhe.query.order_by(order_column).paginate(page=page, per_page=8)
    else:
      dados = Detalhe.query.paginate(page=page, per_page=8)
    if dados:
      return render_template('lista_detalhe.html', title='Lista de Detalhes', id_mst=id_mst, nome_mst=nome_mst, dados=dados, form=form)
    else:
      flash('Falha no acesso ao banco de dados!', 'danger')
      return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('users.logout'))


@modulo5.route('/modulo5/incluirDetalhe/<int:id_mst>/<string:nome_mst>', methods=['GET', 'POST'])
@login_required
def incluirDetalhe(id_mst, nome_mst):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'warning')
    return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))

  form = IncluiDetalheForm()

  if request.method == 'GET':
    return render_template('inclui_detalhe.html', title='Incluir Detalhe', id_mst=id_mst, nome_mst=nome_mst, form=form)

  if not form.validate_on_submit():
    flash('Falha no aplicativo!' , 'danger')
    return render_template('inclui_detalhe.html', title='Incluir Detalhe', id_mst=id_mst, nome_mst=nome_mst, form=form)

  if form.validate_on_submit():
    try:
      dado = Detalhe(nome=form.nome.data, endereco=form.endereco.data, bairro=form.bairro.data,
       cidade=form.cidade.data, telefone=form.telefone.data, mestre_id=id_mst)
      db.session.add(dado)
      db.session.commit()
      flash('Registro foi incluído com sucesso!', 'success')
      return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))


@modulo5.route('/modulo5/incluirDetalhe2/<int:id_mst>/<string:nome_mst>', methods=['GET', 'POST'])
@login_required
def incluirDetalhe2(id_mst, nome_mst):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'warning')
    return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))

  form = IncluiDetalheForm2()

  if request.method == 'GET':
    form.mestre.process_data(id_mst)
    return render_template('inclui_detalhe2.html', title='Incluir Detalhe', id_mst=id_mst, nome_mst=nome_mst, form=form)

  if not form.validate_on_submit():
    flash('Falha no aplicativo!' , 'danger')
    return render_template('inclui_detalhe2.html', title='Incluir Detalhe', id_mst=id_mst, nome_mst=nome_mst, form=form)

  if form.validate_on_submit():
    try:
      dado = Detalhe(nome=form.nome.data, endereco=form.endereco.data, bairro=form.bairro.data,
       cidade=form.cidade.data, telefone=form.telefone.data, mestre_id=form.mestre.data)
      db.session.add(dado)
      db.session.commit()
      flash('Registro foi incluído com sucesso!', 'success')
      return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))


@modulo5.route("/modulo5/excluirDetalhe/<int:id_dado>/<int:id_mst>/<string:nome_mst>", methods=['POST'])
@login_required
def excluirDetalhe(id_dado, id_mst, nome_mst):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'warning')
    return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))

  try:
    dado = Detalhe.query.get(id_dado)
    if dado:
      db.session.delete(dado)
      db.session.commit()
      flash('Registro foi excluido com sucesso!', 'success')
      return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))
    else:
      flash('Falha na exclusão!', 'danger')
      return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))


@modulo5.route('/modulo5/alterarDetalhe/<int:id_dado>/<int:id_mst>/<string:nome_mst>', methods=['GET', 'POST'])
@login_required
def alterarDetalhe(id_dado, id_mst, nome_mst):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'warning')
    return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))

  form = AlteraDetalheForm()

  if request.method == 'GET':
    try:
      dado = Detalhe.query.get(id_dado)
      form.nome.data = dado.nome
      form.endereco.data = dado.endereco
      form.bairro.data = dado.bairro
      form.cidade.data = dado.cidade
      form.telefone.data = dado.telefone
      return render_template('altera_detalhe.html', title='Alterar Detalhe', id_mst=id_mst, nome_mst=nome_mst, form=form)
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))

  if not form.validate_on_submit():
    flash('Falha no aplicativo!' , 'danger')
    return render_template('altera_detalhe.html', title='Alterar Detalhe', id_mst=id_mst, nome_mst=nome_mst, form=form)

  if form.validate_on_submit():
    try:
      dado = Detalhe.query.get(id_dado)
      dado.nome = form.nome.data
      dado.endereco = form.endereco.data
      dado.bairro = form.bairro.data
      dado.cidade = form.cidade.data
      dado.telefone = form.telefone.data
      db.session.commit()
      flash('Registro foi alterado com sucesso!', 'success')
      return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))


@modulo5.route('/modulo5/alterarDetalhe2/<int:id_dado>/<int:id_mst>/<string:nome_mst>', methods=['GET', 'POST'])
@login_required
def alterarDetalhe2(id_dado, id_mst, nome_mst):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'warning')
    return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))

  form = AlteraDetalheForm2()

  if request.method == 'GET':
    try:
      dado = Detalhe.query.get(id_dado)
      form.mestre.process_data(dado.id)
      form.nome.data = dado.nome
      form.endereco.data = dado.endereco
      form.bairro.data = dado.bairro
      form.cidade.data = dado.cidade
      form.telefone.data = dado.telefone
      return render_template('altera_detalhe2.html', title='Alterar Detalhe', id_mst=id_mst, nome_mst=nome_mst, form=form)
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))

  if not form.validate_on_submit():
    flash('Falha no aplicativo!' , 'danger')
    return render_template('altera_detalhe2.html', title='Alterar Detalhe', id_mst=id_mst, nome_mst=nome_mst, form=form)

  if form.validate_on_submit():
    try:
      dado = Detalhe.query.get(id_dado)
      dado.mestre_id = form.mestre.data
      dado.nome = form.nome.data
      dado.endereco = form.endereco.data
      dado.bairro = form.bairro.data
      dado.cidade = form.cidade.data
      dado.telefone = form.telefone.data
      db.session.commit()
      flash('Registro foi alterado com sucesso!', 'success')
      return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))


def imprimir2(id_mst, nome_mst):

  from app_modelo.principal.relatorios import imprimir_reportlab

  ordenarpor = request.form.get('ordenarpor')
  ordem = request.form.get('ordem')
  pesquisarpor = request.form.get('pesquisarpor')

  # LÊ BASE DE DADOS
  try:
    if ordenarpor and ordem and pesquisarpor:
      order_column = text(ordenarpor + ' ' + ordem)
      filter_column = text(ordenarpor + ' LIKE ' + "'%" + pesquisarpor + "%'")
      dados = Detalhe.query.order_by(order_column).filter(filter_column).all()
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Detalhe.query.order_by(order_column).all()
    else:
      dados = Detalhe.query.all()
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo5.acessarDetalhe', id_mst=id_mst, nome_mst=nome_mst))

  # # # PARÂMETROS DO RELATÓRIO
  titulo = 'LISTA DE DETALHES'
  subtitulo = 'Mestre: ' + nome_mst
  lista = [
    ['ID', 'row.id', 50, 80],
    ['NOME', 'row.nome', 100, 200],
    ['CIDADE', 'row.cidade', 220, 300]
  ]

  response = imprimir_reportlab(titulo, subtitulo, lista, dados)
  return response
