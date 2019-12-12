from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from sqlalchemy.exc import IntegrityError
from sqlalchemy import desc, asc, text
from app_modelo import db
from app_modelo.modulo6.models import Professor, Aluno
from app_modelo.modulo6.forms import ListaProfessorForm, IncluiProfessorForm, AlteraProfessorForm, \
  ListaAlunoForm, IncluiAlunoForm, AlteraAlunoForm
import os

modulo6 = Blueprint('modulo6', __name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))


@modulo6.route('/index6', methods=['GET'])
@login_required
def index():
  try:
    return render_template('modulo6.html', title='Modulo 6')
  except TemplateNotFound:
    abort(404)

# # #    PROFESSOR    # # # # # # # # # # # # # # # # # # #
@modulo6.route('/modulo6/acessarProfessor', methods=['GET', 'POST'])
@login_required
def acessarProfessor():

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo6.acessarProfessor'))

  form = ListaProfessorForm()

  title='Lista de Professores'

  data1 = request.form.get('ordenarpor')
  data2 = request.form.get('ordem')
  data3 = request.form.get('pesquisarpor')

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
    form.ordenarpor.data = 'professor_prf.id_prf'
    form.ordenarpor.data = 'ASC'
    form.ordenarpor.data = None
    return redirect(url_for('modulo6.acessarProfessor'))

  try:
    page = request.form.get('page', 1, type=int)
    if data1 and data2 and data3:
      order_column = text(data1 + ' ' + data2)
      filter_column = text(data1 + ' LIKE ' + "'%" + data3 + "%'")
      dados = Professor.query.order_by(order_column).filter(filter_column).paginate(page=page, per_page=8)
    elif data1 and data2:
      order_column = text(data1 + ' ' + data2)
      dados = Professor.query.order_by(order_column).paginate(page=page, per_page=8)
    else:
      dados = Professor.query.paginate(page=page, per_page=8)
    if dados:
      return render_template('lista_professor.html', title=title, dados=dados, form=form)
    else:
      flash('Falha no acesso ao banco de dados!', 'danger')
      return redirect(url_for('modulo6.acessarProfessor'))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('users.logout'))


@modulo6.route('/modulo6/incluirProfessor', methods=['GET', 'POST'])
@login_required
def incluirProfessor():

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo6.acessarProfessor'))

  form = IncluiProfessorForm()

  title='Incluir Professor'

  if request.method == 'GET':
    return render_template('inclui_professor.html', title=title, form=form)

  if not form.validate_on_submit():
    return render_template('inclui_professor.html', title=title, form=form)
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
      return redirect(url_for('modulo6.acessarProfessor'))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo6.acessarProfessor'))


@modulo6.route("/modulo6/excluirProfessor/<int:id_data>", methods=['POST'])
@login_required
def excluirProfessor(id_data):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo6.acessarProfessor'))

  try:
    dado = Professor.query.get(id_data)
    if dado:
      db.session.delete(dado)
      db.session.commit()
      flash('Registro foi excluido com sucesso!', 'success')
      return redirect(url_for('modulo6.acessarProfessor'))
    else:
      flash('Falha na exclusão!', 'danger')
      return redirect(url_for('modulo6.acessarProfessor'))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo6.acessarProfessor'))


@modulo6.route('/modulo6/alterarProfessor/<int:id_data>', methods=['GET', 'POST'])
@login_required
def alterarProfessor(id_data):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo6.acessarProfessor'))

  form = AlteraProfessorForm()

  title='Alterar Professor'

  if request.method == 'GET':
    try:
      dado = Professor.query.get(id_data)
      form.nome.data = dado.nome
      return render_template('altera_professor.html', title=title, form=form)
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo6.acessarProfessor'))

  if not form.validate_on_submit():
    return render_template('altera_professor.html', title=title, form=form)

  if form.validate_on_submit():
      try:
        dado = Professor.query.get(id_data)
        dado.nome = form.nome.data
        db.session.commit()
        flash('Registro foi alterado com sucesso!', 'success')
        return redirect(url_for('modulo6.acessarProfessor'))
      except Exception as e:
        flash('Falha no aplicativo! ' + str(e), 'danger')
        return redirect(url_for('modulo6.acessarProfessor'))

def imprimir1():

  from app_modelo.principal.relatorios import imprimir_reportlab

  data1 = request.form.get('ordenarpor')
  data2 = request.form.get('ordem')
  data3 = request.form.get('pesquisarpor')

  # LÊ BASE DE DADOS
  try:
    if data1 and data2 and data3:
      order_column = text(data1 + ' ' + data2)
      filter_column = text(data1 + ' LIKE ' + "'%" + data3 + "%'")
      dados = Professor.query.order_by(order_column).filter(filter_column).all()
    elif data1 and data2:
      order_column = text(data1 + ' ' + data2)
      dados = Professor.query.order_by(order_column).all()
    else:
      dados = Professor.query.all()
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo6.acessarProfessor'))

  # # # PARÂMETROS DO RELATÓRIO
  titulo = 'LISTA DE PROFESSORES'
  subtitulo = None
  lista = [
    ['ID', 'row.id', 50, 80],
    ['NOME', 'row.nome', 100, 200]
  ]

  response = imprimir_reportlab(titulo, subtitulo, lista, dados)
  return response

# # #    ALUNO    # # # # # # # # # # # # # # # # # # #
@modulo6.route('/modulo6/acessarAluno/<int:id_super>/<string:nome_super>', methods=['GET', 'POST'])
@login_required
def acessarAluno(id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))

  form = ListaAlunoForm()

  data1_aluno = request.form.get('ordenarpor_aluno')
  data2_aluno = request.form.get('ordem_aluno')
  data3_aluno = request.form.get('pesquisarpor_aluno')
  submit_enviar_aluno = request.form.get('submit_enviar_aluno')
  submit_limpar_aluno = request.form.get('submit_limpar_aluno')

  data1_aluno_professor = request.form.get('ordenarpor_aluno_professor')
  data2_aluno_professor = request.form.get('ordem_aluno_professor')
  data3_aluno_professor = request.form.get('pesquisarpor_aluno_professor')
  submit_enviar_aluno_professor = request.form.get('submit_enviar_aluno_professor')
  submit_limpar_aluno_professor = request.form.get('submit_limpar_aluno_professor')

  try:
    imprimir_aluno = request.form.get('imprimir_aluno')
    if imprimir_aluno:
      response = imprimir_alunos(id_super, nome_super)
      return response
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('conta.logout'))

  try:
    imprimir_aluno_professor = request.form.get('imprimir_aluno_professor')
    if imprimir_aluno_professor:
      response = imprimir_alunos_professor(id_super, nome_super)
      return response
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('conta.logout'))

  submit_limpar_aluno = request.form.get('submit_limpar_aluno')
  if submit_limpar_aluno:
    form.ordenarpor_aluno.data = 'aluno_aln.id_aln'
    form.ordem_aluno.data = 'ASC'
    form.pesquisarpor_aluno.data = None
    return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))

  submit_limpar_aluno_professor = request.form.get('submit_limpar_aluno_professor')
  if submit_limpar_aluno_professor:
    form.ordenarpor_aluno_professor.data = 'aluno_aln.id_aln'
    form.ordem_aluno_professor.data = 'ASC'
    form.pesquisarpor_aluno_professor.data = None
    return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))

  title1='Lista de Alunos Por Professor'
  title2='Lista de Alunos'

  try:

    page = request.form.get('page', 1, type=int)
    if data1_aluno_professor and data2_aluno_professor and data3_aluno_professor:
      order_column = text(data1_aluno_professor + ' ' + data2_aluno_professor)
      filter_column = text(data1_aluno_professor + ' LIKE ' + "'%" + data3_aluno_professor + "%'")
      dados_aluno_professor = Aluno.query.order_by(order_column).filter((Aluno.professores.any(id=id_super)) & (filter_column)).paginate(page=page, per_page=8)
    elif data1_aluno_professor and data2_aluno_professor:
      order_column = text(data1_aluno_professor + ' ' + data2_aluno_professor)
      dados_aluno_professor = Aluno.query.order_by(order_column).filter(Aluno.professores.any(id=id_super)).paginate(page=page, per_page=8)
    else:
      dados_aluno_professor = Aluno.query.filter(Aluno.professores.any(id=id_super)).paginate(page=page, per_page=8)

    if data1_aluno and data2_aluno and data3_aluno:
      order_column = text(data1_aluno + ' ' + data2_aluno)
      filter_column = text(data1_aluno + ' LIKE ' + "'%" + data3_aluno + "%'")
      dados_aluno = Aluno.query.order_by(order_column).filter(filter_column).paginate(page=page, per_page=8)
    elif data1_aluno and data2_aluno:
      order_column = text(data1_aluno + ' ' + data2_aluno)
      dados_aluno = Aluno.query.order_by(order_column).paginate(page=page, per_page=8)
    else:
      dados_aluno = Aluno.query.paginate(page=page, per_page=8)

    return render_template('lista_aluno.html', title1=title1, title2=title2, id_super=id_super, nome_super=nome_super, dados1=dados_aluno_professor, dados2=dados_aluno, form=form)

  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('users.logout'))


@modulo6.route('/modulo6/incluirAluno/<int:id_super>/<string:nome_super>', methods=['GET', 'POST'])
@login_required
def incluirAluno(id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))

  form = IncluiAlunoForm()

  title='Incluir Aluno'

  if request.method == 'GET':
    return render_template('inclui_aluno.html', title=title, id_super=id_super, nome_super=nome_super, form=form)

  if not form.validate_on_submit():
    return render_template('inclui_aluno.html', title=title, id_super=id_super, nome_super=nome_super, form=form)

  if form.validate_on_submit():
    try:
      dado = Aluno(nome=form.nome.data)
      db.session.add(dado)
      db.session.commit()
      flash('Registro foi incluído com sucesso!', 'success')
      return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))


@modulo6.route('/modulo6/adicionarAluno/<int:id_data>/<int:id_super>/<string:nome_super>', methods=['GET', 'POST'])
@login_required
def adicionarAluno(id_data, id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))

  try:
    dado = Professor.query.get(id_super)
    dado1 = Aluno.query.get(id_data)
    dado1.professores.append(dado)
    db.session.commit()
    flash('Registro foi incluído com sucesso!', 'success')
    return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))
  except IntegrityError:
    db.session.rollback()
    flash('Registro já cadastrado! ', 'danger')
    return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))


@modulo6.route("/modulo6/excluirAlunoProfessor/<int:id_data>/<int:id_super>/<string:nome_super>", methods=['POST'])
@login_required
def excluirAlunoProfessor(id_data, id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))

  try:
    dado = Professor.query.get(id_super)
    dado1 = Aluno.query.get(id_data)
    if dado:
      # exclui somente da tabela de associação
      dado1.professores.remove(dado)
      db.session.commit()
      flash('Registro foi excluido com sucesso!', 'success')
      return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))
    else:
      flash('Falha na exclusão!', 'danger')
      return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))


@modulo6.route("/modulo6/excluirAluno/<int:id_data>/<int:id_super>/<string:nome_super>", methods=['POST'])
@login_required
def excluirAluno(id_data, id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))

  try:
    dado = Aluno.query.get(id_data)
    if dado:
      # exclui da tabela de aluno e, automaticamente, da tabela de associação
      db.session.delete(dado)
      db.session.commit()
      flash('Registro foi excluido com sucesso!', 'success')
      return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))
    else:
      flash('Falha na exclusão!', 'danger')
      return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))


@modulo6.route('/modulo6/alterarAluno/<int:id_data>/<int:id_super>/<string:nome_super>', methods=['GET', 'POST'])
@login_required
def alterarAluno(id_data, id_super, nome_super):

  if not current_user.is_authenticated:
    flash('Usuário não autorizado!', 'info')
    return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))

  form = AlteraAlunoForm()

  title='Alterar Aluno'

  if request.method == 'GET':
    try:
      dado = Aluno.query.get(id_data)
      form.nome.data = dado.nome
      return render_template('altera_aluno.html', title=title, id_super=id_super, nome_super=nome_super, form=form)
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
      return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))

  if not form.validate_on_submit():
    return render_template('altera_aluno.html', title=title, id_super=id_super, nome_super=nome_super, form=form)

  if form.validate_on_submit():
      try:
        dado = Aluno.query.get(id_data)
        dado.nome = form.nome.data
        db.session.commit()
        flash('Registro foi alterado com sucesso!', 'success')
        return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))
      except Exception as e:
        flash('Falha no aplicativo! ' + str(e), 'danger')
        return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))


def imprimir_alunos(id_super, nome_super):

  from app_modelo.principal.relatorios import imprimir_reportlab

  data1 = request.form.get('ordenarpor_aluno')
  data2 = request.form.get('ordem_aluno')
  data3 = request.form.get('pesquisarpor_aluno')

  # LÊ BASE DE DADOS
  try:
    if data1 and data2 and data3:
      order_column = text(data1 + ' ' + data2)
      filter_column = text(data1 + ' LIKE ' + "'%" + data3 + "%'")
      dados = Aluno.query.order_by(order_column).filter(filter_column).all()
    elif data1 and data2:
      order_column = text(data1 + ' ' + data2)
      dados = Aluno.query.order_by(order_column).all()
    else:
      dados = Aluno.query.all()
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))

  # # # PARÂMETROS DO RELATÓRIO
  titulo = 'LISTA DE ALUNOS'
  subtitulo = None
  lista = [
    ['ID', 'row.id', 50, 80],
    ['NOME', 'row.nome', 100, 200]
  ]

  response = imprimir_reportlab(titulo, subtitulo, lista, dados)
  return response


def imprimir_alunos_professor(id_super, nome_super):

  from app_modelo.principal.relatorios import imprimir_reportlab

  data1 = request.form.get('ordenarpor_aluno_professor')
  data2 = request.form.get('ordem_aluno_professor')
  data3 = request.form.get('pesquisarpor_aluno_professor')

  # LÊ BASE DE DADOS
  try:
    if data1 and data2 and data3:
      order_column = text(data1 + ' ' + data2)
      filter_column = text(data1 + ' LIKE ' + "'%" + data3 + "%'")
      dados = Aluno.query.order_by(order_column).filter((Aluno.professores.any(id=id_super)) & (filter_column)).all()
    elif data1 and data2:
      order_column = text(data1 + ' ' + data2)
      dados = Aluno.query.order_by(order_column).filter(Aluno.professores.any(id=id_super)).all()
    else:
      dados = Aluno.query.filter(Aluno.professores.any(id=id_super)).all()
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo6.acessarAluno', id_super=id_super, nome_super=nome_super))

  # # # PARÂMETROS DO RELATÓRIO
  titulo = 'LISTA DE ALUNOS POR PROFESSOR'
  subtitulo = 'Professor: ' + nome_super
  lista = [
    ['ID', 'row.id', 50, 80],
    ['NOME', 'row.nome', 100, 200]
  ]

  response = imprimir_reportlab(titulo, subtitulo, lista, dados)
  return response
