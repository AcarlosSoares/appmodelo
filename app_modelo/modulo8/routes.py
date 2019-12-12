from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, asc, text
from app_modelo import db
from app_modelo.modulo6.models import Professor, Aluno
from app_modelo.modulo8.forms import ListaProfessorForm, IncluiProfessorForm, AlteraProfessorForm, \
  ListaAlunoForm, IncluiAlunoForm, AlteraAlunoForm, ListaAlunosPorProfessorForm
import os

modulo8 = Blueprint('modulo8', __name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))


@modulo8.route('/index6', methods=['GET'])
@login_required
def index():
  try:
    return render_template('modulo8.html', title='Modulo 8')
  except TemplateNotFound:
    abort(404)


# # #    PROFESSOR    # # # # # # # # # # # # # # # # # # #
@modulo8.route('/modulo8/acessarProfessor', methods=['GET', 'POST'])
@login_required
def acessarProfessor():

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo8.acessarProfessor'))

  form = ListaProfessorForm()

  title='Lista de Professores'

  ordenarpor = request.form.get('ordenarpor')
  ordem = request.form.get('ordem')
  pesquisarpor = request.form.get('pesquisarpor')
  imprimir = request.form.get('imprimir')

  if imprimir:
    response = imprimir1()
    return response

  limpar = request.form.get('submit_limpar')
  if limpar:
    form.ordenarpor.data = 'professor_prf.id_prf'
    form.ordenarpor.data = 'ASC'
    form.ordenarpor.data = None
    return redirect(url_for('modulo8.acessarProfessor'))

  try:
    page = request.form.get('page', 1, type=int)
    if ordenarpor and ordem and pesquisarpor:
      order_column = text(ordenarpor + ' ' + ordem)
      filter_column = text(ordenarpor + ' LIKE ' + "'%" + pesquisarpor + "%'")
      dados = Professor.query.order_by(order_column).filter(filter_column).paginate(page=page, per_page=8)
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Professor.query.order_by(order_column).paginate(page=page, per_page=8)
    else:
      dados = Professor.query.paginate(page=page, per_page=8)
    if dados:
      return render_template('mod8_lista_professor.html', title=title, dados=dados, form=form)
    else:
      flash('Falha no acesso ao banco de dados!', 'danger')
      return redirect(url_for('modulo8.acessarProfessor'))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('users.logout'))


@modulo8.route('/modulo8/incluirProfessor', methods=['GET', 'POST'])
@login_required
def incluirProfessor():

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo8.acessarProfessor'))

  form = IncluiProfessorForm()

  title='Incluir Professor'

  if request.method == 'GET':
    return render_template('mod8_inclui_professor.html', title=title, form=form)

  if not form.validate_on_submit():
    return render_template('mod8_inclui_professor.html', title=title, form=form)
    # for fieldName, errorMessages in form.errors.items():
    #   for err in errorMessages:
    #     # print('* * * ERRO: campo: ' + fieldName + ' - mensagem: ' + err)
    #     msg = ' ERRO: campo: ' + fieldName + ' - mensagem: ' + err
    # flash('Formulário não validado! ' + msg, 'danger')

  if form.validate_on_submit():
    try:
      dado = Professor(nome=form.nome.data)
      db.session.add(dado)
      db.session.commit()
      flash('Registro foi incluído com sucesso!', 'success')
      return redirect(url_for('modulo8.acessarProfessor'))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo8.acessarProfessor'))


@modulo8.route("/modulo8/excluirProfessor/<int:id_data>", methods=['POST'])
@login_required
def excluirProfessor(id_data):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo8.acessarProfessor'))

  try:
    dado = Professor.query.get(id_data)
    if dado:
      db.session.delete(dado)
      db.session.commit()
      flash('Registro foi excluido com sucesso!', 'success')
      return redirect(url_for('modulo8.acessarProfessor'))
    else:
      flash('Falha na exclusão!', 'danger')
      return redirect(url_for('modulo8.acessarProfessor'))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo8.acessarProfessor'))


@modulo8.route('/modulo8/alterarProfessor/<int:id_data>', methods=['GET', 'POST'])
@login_required
def alterarProfessor(id_data):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo8.acessarProfessor'))

  form = AlteraProfessorForm()

  title='Alterar Professor'

  if request.method == 'GET':
    try:
      dado = Professor.query.get(id_data)
      form.nome.data = dado.nome
      return render_template('mod8_altera_professor.html', title=title, form=form)
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo8.acessarProfessor'))

  if not form.validate_on_submit():
    return render_template('mod8_altera_professor.html', title=title, form=form)

  if form.validate_on_submit():
      try:
        dado = Professor.query.get(id_data)
        dado.nome = form.nome.data
        db.session.commit()
        flash('Registro foi alterado com sucesso!', 'success')
        return redirect(url_for('modulo8.acessarProfessor'))
      except Exception as e:
        flash('Falha no aplicativo! ' + str(e), 'danger')
        return redirect(url_for('modulo8.acessarProfessor'))


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
      dados = Professor.query.order_by(order_column).filter(filter_column).all()
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Professor.query.order_by(order_column).all()
    else:
      dados = Professor.query.all()
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo8.acessarProfessor'))

  # # # PARÂMETROS DO RELATÓRIO
  titulo = 'LISTA DE PROFESSORES'
  subtitulo = None
  lista = [
    ['ID', 'row.id', 50, 80],
    ['NOME', 'row.nome', 100, 200]
  ]

  response = imprimir_reportlab(titulo, subtitulo, lista, dados)
  return response


# # #    ALUNOS POR PROFESSOR    # # # # # # # # # # # # # # # # # # #
@modulo8.route('/modulo8/acessarAlunosPorProfessor/<int:id_super>/<string:nome_super>', methods=['GET', 'POST'])
@login_required
def acessarAlunosPorProfessor(id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo8.acessarAlunosPorProfessor', id_super=id_super, nome_super=nome_super))

  form = ListaAlunosPorProfessorForm()

  ordenarpor = request.form.get('ordenarpor')
  ordem = request.form.get('ordem')
  pesquisarpor = request.form.get('pesquisarpor')
  submit_enviar = request.form.get('submit_enviar')
  submit_limpar = request.form.get('submit_limpar')
  imprimir = request.form.get('imprimir')

  if imprimir:
    response = imprimir2(id_super, nome_super)
    return response

  if submit_limpar:
    form.ordenarpor.data = 'aluno_aln.id_aln'
    form.ordem.data = 'ASC'
    form.pesquisarpor.data = None
    return redirect(url_for('modulo8.acessarAlunosPorProfessor', id_super=id_super, nome_super=nome_super))

  title='Lista de Alunos Por Professor'

  try:
    page = request.form.get('page', 1, type=int)
    if ordenarpor and ordem and pesquisarpor:
      order_column = text(ordenarpor + ' ' + ordem)
      filter_column = text(ordenarpor + ' LIKE ' + "'%" + pesquisarpor + "%'")
      dados = Aluno.query.order_by(order_column).filter((Aluno.professores.any(id=id_super)) & (filter_column)).paginate(page=page, per_page=8)
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Aluno.query.order_by(order_column).filter(Aluno.professores.any(id=id_super)).paginate(page=page, per_page=8)
    else:
      dados = Aluno.query.filter(Aluno.professores.any(id=id_super)).paginate(page=page, per_page=8)

    return render_template('mod8_lista_alunosporprofessor.html', title=title, id_super=id_super, nome_super=nome_super, dados=dados, form=form)

  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('users.logout'))


@modulo8.route("/modulo8/excluirAlunoProfessor/<int:id_data>/<int:id_super>/<string:nome_super>", methods=['POST'])
@login_required
def excluirAlunoProfessor(id_data, id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo8.acessarAlunosPorProfessor', id_super=id_super, nome_super=nome_super))

  try:
    dado = Professor.query.get(id_super)
    dado1 = Aluno.query.get(id_data)
    if dado:
      # exclui somente da tabela de associação
      dado1.professores.remove(dado)
      db.session.commit()
      flash('Registro foi excluido com sucesso!', 'success')
      return redirect(url_for('modulo8.acessarAlunosPorProfessor', id_super=id_super, nome_super=nome_super))
    else:
      flash('Falha na exclusão!', 'danger')
      return redirect(url_for('modulo8.acessarAlunosPorProfessor', id_super=id_super, nome_super=nome_super))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo8.acessarAlunosPorProfessor', id_super=id_super, nome_super=nome_super))


def imprimir2(id_super, nome_super):

  from app_modelo.principal.relatorios import imprimir_reportlab

  ordenarpor = request.form.get('ordenarpor')
  ordem = request.form.get('ordem')
  pesquisarpor = request.form.get('pesquisarpor')

  # LÊ BASE DE DADOS
  try:
    if ordenarpor and ordem and pesquisarpor:
      order_column = text(ordenarpor + ' ' + ordem)
      filter_column = text(ordenarpor + ' LIKE ' + "'%" + pesquisarpor + "%'")
      dados = Aluno.query.order_by(order_column).filter((Aluno.professores.any(id=id_super)) & (filter_column)).all()
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Aluno.query.order_by(order_column).filter(Aluno.professores.any(id=id_super)).all()
    else:
      dados = Aluno.query.filter(Aluno.professores.any(id=id_super)).all()
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo8.acessarAluno', id_super=id_super, nome_super=nome_super))

  # # # PARÂMETROS DO RELATÓRIO
  titulo = 'LISTA DE ALUNOS POR PROFESSOR'
  subtitulo = 'Professor: ' + nome_super
  lista = [
    ['ID', 'row.id', 50, 80],
    ['NOME', 'row.nome', 100, 200]
  ]

  response = imprimir_reportlab(titulo, subtitulo, lista, dados)
  return response


# # #    ALUNO    # # # # # # # # # # # # # # # # # # #
@modulo8.route('/modulo8/acessarAluno/<int:id_super>/<string:nome_super>', methods=['GET', 'POST'])
@login_required
def acessarAluno(id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo8.acessarAluno', id_super=id_super, nome_super=nome_super))

  form = ListaAlunoForm()

  ordenarpor = request.form.get('ordenarpor')
  ordem = request.form.get('ordem')
  pesquisarpor = request.form.get('pesquisarpor')
  submit_enviar = request.form.get('submit_enviar')
  submit_limpar = request.form.get('submit_limpar')
  imprimir = request.form.get('imprimir')

  if imprimir:
    response = imprimir3(id_super, nome_super)
    return response

  if submit_limpar:
    form.ordenarpor.data = 'aluno_aln.id_aln'
    form.ordem.data = 'ASC'
    form.pesquisarpor.data = None
    return redirect(url_for('modulo8.acessarAluno', id_super=id_super, nome_super=nome_super))

  title2='Lista de Alunos'

  try:

    page = request.form.get('page', 1, type=int)
    if ordenarpor and ordem and pesquisarpor:
      order_column = text(ordenarpor + ' ' + ordem)
      filter_column = text(ordenarpor + ' LIKE ' + "'%" + pesquisarpor + "%'")
      dados = Aluno.query.order_by(order_column).filter(filter_column).paginate(page=page, per_page=8)
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Aluno.query.order_by(order_column).paginate(page=page, per_page=8)
    else:
      dados = Aluno.query.paginate(page=page, per_page=8)

    return render_template('mod8_lista_aluno.html', title2=title2, id_super=id_super, nome_super=nome_super, dados2=dados, form=form)

  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('users.logout'))


@modulo8.route('/modulo8/incluirAluno/<int:id_super>/<string:nome_super>', methods=['GET', 'POST'])
@login_required
def incluirAluno(id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo8.acessarAluno', id_super=id_super, nome_super=nome_super))

  form = IncluiAlunoForm()

  title='Incluir Aluno'

  if request.method == 'GET':
    return render_template('mod8_inclui_aluno.html', title=title, id_super=id_super, nome_super=nome_super, form=form)

  if not form.validate_on_submit():
    return render_template('mod8_inclui_aluno.html', title=title, id_super=id_super, nome_super=nome_super, form=form)

  if form.validate_on_submit():
    try:
      dado = Aluno(nome=form.nome.data)
      db.session.add(dado)
      db.session.commit()
      flash('Registro foi incluído com sucesso!', 'success')
      return redirect(url_for('modulo8.acessarAluno', id_super=id_super, nome_super=nome_super))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo8.acessarAluno', id_super=id_super, nome_super=nome_super))


@modulo8.route('/modulo8/adicionarAluno/<int:id_data>/<int:id_super>/<string:nome_super>', methods=['GET', 'POST'])
@login_required
def adicionarAluno(id_data, id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo8.acessarAluno', id_super=id_super, nome_super=nome_super))

  try:
    dado = Professor.query.get(id_super)
    dado1 = Aluno.query.get(id_data)
    dado1.professores.append(dado)
    db.session.commit()
    flash('Registro foi incluído com sucesso!', 'success')
    return redirect(url_for('modulo8.acessarAlunosPorProfessor', id_super=id_super, nome_super=nome_super))
  except IntegrityError:
    db.session.rollback()
    flash('Registro já cadastrado! ', 'danger')
    return redirect(url_for('modulo8.acessarAluno', id_super=id_super, nome_super=nome_super))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo8.acessarAluno', id_super=id_super, nome_super=nome_super))


@modulo8.route("/modulo8/excluirAluno/<int:id_data>/<int:id_super>/<string:nome_super>", methods=['POST'])
@login_required
def excluirAluno(id_data, id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo8.acessarAluno', id_super=id_super, nome_super=nome_super))

  try:
    dado = Aluno.query.get(id_data)
    if dado:
      # exclui da tabela de aluno e, automaticamente, da tabela de associação
      db.session.delete(dado)
      db.session.commit()
      flash('Registro foi excluido com sucesso!', 'success')
      return redirect(url_for('modulo8.acessarAluno', id_super=id_super, nome_super=nome_super))
    else:
      flash('Falha na exclusão!', 'danger')
      return redirect(url_for('modulo8.acessarAluno', id_super=id_super, nome_super=nome_super))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo8.acessarAluno', id_super=id_super, nome_super=nome_super))


@modulo8.route('/modulo8/alterarAluno/<int:id_data>/<int:id_super>/<string:nome_super>', methods=['GET', 'POST'])
@login_required
def alterarAluno(id_data, id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo8.acessarAluno', id_super=id_super, nome_super=nome_super))

  form = AlteraAlunoForm()

  title='Alterar Aluno'

  if request.method == 'GET':
    try:
      dado = Aluno.query.get(id_data)
      form.nome.data = dado.nome
      return render_template('mod8_altera_aluno.html', title=title, id_super=id_super, nome_super=nome_super, form=form)
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo8.acessarAluno', id_super=id_super, nome_super=nome_super))

  if not form.validate_on_submit():
    return render_template('mod8_altera_aluno.html', title=title, id_super=id_super, nome_super=nome_super, form=form)

  if form.validate_on_submit():
      try:
        dado = Aluno.query.get(id_data)
        dado.nome = form.nome.data
        db.session.commit()
        flash('Registro foi alterado com sucesso!', 'success')
        return redirect(url_for('modulo8.acessarAluno', id_super=id_super, nome_super=nome_super))
      except Exception as e:
        flash('Falha no aplicativo! ' + str(e), 'danger')
        return redirect(url_for('modulo8.acessarAluno', id_super=id_super, nome_super=nome_super))


def imprimir3(id_super, nome_super):

  from app_modelo.principal.relatorios import imprimir_reportlab

  ordenarpor = request.form.get('ordenarpor')
  ordem = request.form.get('ordem')
  pesquisarpor = request.form.get('pesquisarpor')

  # LÊ BASE DE DADOS
  try:
    if ordenarpor and ordem and pesquisarpor:
      order_column = text(ordenarpor + ' ' + ordem)
      filter_column = text(ordenarpor + ' LIKE ' + "'%" + pesquisarpor + "%'")
      dados = Aluno.query.order_by(order_column).filter(filter_column).all()
    elif ordenarpor and ordem:
      order_column = text(ordenarpor + ' ' + ordem)
      dados = Aluno.query.order_by(order_column).all()
    else:
      dados = Aluno.query.all()
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo8.acessarAluno', id_super=id_super, nome_super=nome_super))

  # # # PARÂMETROS DO RELATÓRIO
  titulo = 'LISTA DE ALUNOS'
  subtitulo = None
  lista = [
    ['ID', 'row.id', 50, 80],
    ['NOME', 'row.nome', 100, 200]
  ]

  response = imprimir_reportlab(titulo, subtitulo, lista, dados)
  return response
