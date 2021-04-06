from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from .models import db
from book_reviewer.background.tasks import mail
from .config import Config
from book_reviewer.background.celery_utils import init_celery

jwt_manager = JWTManager()
bcrypt = Bcrypt()


def create_app(config_class=Config, **kwargs):
    app = Flask(__name__)
    app.config.from_object(config_class)
    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), app)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt_manager.init_app(app)
    mail.init_app(app)

    from book_reviewer.auth.routes import auth
    from book_reviewer.books.routes import books
    from book_reviewer.errors.handlers import errors
    app.register_blueprint(auth)
    app.register_blueprint(books)
    app.register_blueprint(errors)

    return app
