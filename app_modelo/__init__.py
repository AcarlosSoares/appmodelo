from flask import Flask
from app_modelo.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
login_manager.login_message = "Faça o Login para acessar esta página!"

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app_modelo.principal.routes import principal
    from app_modelo.errors.handlers import errors
    from app_modelo.users.routes import users
    from app_modelo.modulo1.routes import modulo1
    from app_modelo.modulo2.routes import modulo2
    from app_modelo.modulo3.routes import modulo3
    from app_modelo.modulo4.routes import modulo4
    from app_modelo.modulo5.routes import modulo5
    from app_modelo.modulo6.routes import modulo6
    from app_modelo.modulo7.routes import modulo7
    from app_modelo.modulo8.routes import modulo8
    from app_modelo.tb_empresa_emp.routes import tb_empresa_emp
    app.register_blueprint(principal)
    app.register_blueprint(errors)
    app.register_blueprint(users)
    app.register_blueprint(modulo1)
    app.register_blueprint(modulo2)
    app.register_blueprint(modulo3)
    app.register_blueprint(modulo4)
    app.register_blueprint(modulo5)
    app.register_blueprint(modulo6)
    app.register_blueprint(modulo7)
    app.register_blueprint(modulo8)
    app.register_blueprint(tb_empresa_emp)

    return app
