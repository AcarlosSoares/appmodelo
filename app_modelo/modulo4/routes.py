from flask import render_template, Blueprint
from flask_login import current_user, login_required
import os

modulo4 = Blueprint('modulo4', __name__, template_folder=os.path.join(os.path.dirname(__file__), 'templates'))


@modulo4.route('/modulo4', methods=['GET'])
@login_required
def acessar():
    try:
        return render_template('modulo4.html', title='modulo4')
    except TemplateNotFound:
        abort(404)
