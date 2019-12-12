from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app, flash
from app_modelo import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
  try:
    return User.query.get(int(user_id))
  except Exception as e:
    flash('Ocorreu uma falha no acesso ao banco de dados! ' + str(e), 'danger')


class User(db.Model, UserMixin):

    __tablename__ = 'conta_con'

    id = db.Column("id_conta", db.Integer, primary_key=True)
    username = db.Column("ds_usuario_con", db.String(20), unique=True, nullable=False)
    email = db.Column("ds_email_con", db.String(120), unique=True, nullable=False)
    image_file = db.Column("ds_foto_con", db.String(20), nullable=False, default='default.jpg')
    password = db.Column("ds_senha_con", db.String(60), nullable=False)


    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
