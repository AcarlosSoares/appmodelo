from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from app_modelo import db
from app_modelo.modulo3.models import Modelo
from app_modelo.modulo3.forms import ListaModeloForm
import os

modulo3 = Blueprint('modulo3', __name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))


@modulo3.route('/modulo3/acessar', methods=['GET'])
@login_required
def acessar():
  try:
    # print('* * * MODULO 1 Acessar')
    form = ListaModeloForm()
    page = request.args.get('page', 1, type=int)
    # modelos = Modelo.query.order_by(Modelo.sigla.desc()).paginate(page=page, per_page=5)
    modelos = Modelo.query.paginate(page=page, per_page=8)
  except Exception as e:
    flash('Falha no aplicativo! ' + str(e), 'danger')
    return redirect(url_for('modulo3.acessar'))
  return render_template('lista_modelo3.html', title='Lista de Modelos', dados=modelos, form=form)


@modulo3.route('/modulo3/incluir', methods=['GET', 'POST'])
@login_required
def incluir():
  form = ListaModeloForm()
  if form.validate_on_submit():
    try:
      # print('* * * * MODULO 1 Incluir')
      modelo = Modelo(sigla=form.sigla.data, nome=form.nome.data)
      db.session.add(modelo)
      db.session.commit()
      flash('Registro foi incluído com sucesso!', 'success')
      return redirect(url_for('modulo3.acessar'))
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
  else:
    erro_msg = ""
    for field, errors in form.errors.items():
      for error in errors:
        erro_msg = erro_msg + ("%s - %s" % (getattr(form, field).label.text, error)) + "<br/>"
    flash(erro_msg, 'danger')
  return redirect(url_for('modulo3.acessar'))


@modulo3.route("/modulo3/excluir/<int:id_data>", methods=['GET', 'POST'])
@login_required
def excluir(id_data):
  if current_user.is_authenticated:
    try:
      modelo = Modelo.query.get(id_data)
      if modelo:
        db.session.delete(modelo)
        db.session.commit()
        flash('Registro foi excluido com sucesso!', 'success')
        return redirect(url_for('modulo3.acessar'))
      else:
        flash('Falha na exclusão!', 'danger')
    except Exception as e:
      flash('Falha no aplicativo! ' + str(e), 'danger')
  else:
    flash('Usuário não autorizado!', 'info')
  return redirect(url_for('modulo3.acessar'))


@modulo3.route('/modulo3/alterar/<int:id_data>', methods=['GET', 'POST'])
@login_required
def alterar(id_data):
  # print("* * * ID: " + str(id_data))
  form = ListaModeloForm()
  if form.validate_on_submit():
      # print("* * * POST")
      modelo = Modelo.query.get(id_data)
      # modelo = db_session.query(Modelo).filter(Modelo.id==id_data)
      modelo.sigla = form.sigla.data
      modelo.nome = form.nome.data
      db.session.commit()
      flash('Registro foi alterado com sucesso!', 'success')
  elif request.method == 'GET':
      # print("* * * GET")
      modelo = Modelo.query.get(id_data)
      # modelo = db_session.query(Modelo).filter(Modelo.id==id_data)
      form.sigla.data = modelo.sigla
      form.nome.data = modelo.nome
      flash('Registro não foi alterado!', 'danger')
  return redirect(url_for('modulo3.acessar'))
