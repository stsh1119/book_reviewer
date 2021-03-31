from flask import Flask
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from .models import db
from .config import Config

jwt_manager = JWTManager()
bcrypt = Bcrypt()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    jwt_manager.init_app(app)

    from book_reviewer.auth.routes import auth
    from book_reviewer.books.routes import books
    from book_reviewer.errors.handlers import errors
    app.register_blueprint(auth)
    app.register_blueprint(books)
    app.register_blueprint(errors)

    return app
