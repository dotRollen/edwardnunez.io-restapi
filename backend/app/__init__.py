import connexion
from flask_cors import CORS
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_mail import Mail
from backend.config import config

# Instantiating middle dependencie
db = MongoEngine()
mail = Mail()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    connex_app = connexion.FlaskApp(__name__, specification_dir='swagger/')
    connex_app.app.config.from_object(config[config_name])
    config[config_name].init_app(connex_app.app)
    
    CORS(connex_app.app)
    mail.init_app(connex_app.app)
    db.init_app(connex_app.app)
    login_manager.init_app(connex_app.app)

    # if connex_app.app.config['SSL_REDIRECT']:
    #     from flask_sslify import SSLify
    #     sslify = SSLify(app)

    return connex_app
