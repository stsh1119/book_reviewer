from typing import Union
from flask_jwt_extended import create_refresh_token, create_access_token
from sqlalchemy.exc import IntegrityError
from .dto import UserRegisterDto, UserLoginDto, UserChangePwdDto
from book_reviewer.models import db, User
from book_reviewer import bcrypt


def register_user(user: UserRegisterDto) -> None:
    hashed_password = bcrypt.generate_password_hash(user.password).decode('utf-8')
    user = User(email=user.email, password=hashed_password,)
    try:
        db.session.add(user)
        db.session.commit()

    except IntegrityError:
        raise Exception('User with this email is already registered.')


def login_user(user: UserLoginDto) -> Union[dict, str]:
    try:
        db_user = User.query.filter_by(email=user.email).first()
        if not db_user:
            raise Exception('No such login.')

        if not bcrypt.check_password_hash(db_user.password, user.password):
            raise Exception("Error: either login or password is incorrect.")

        response = {
            'access_token': create_access_token(identity=user.email),
            'refresh_token': create_refresh_token(identity=user.email)
        }
        return response

    except Exception as e:
        return str(e)


def change_pwd(user: UserChangePwdDto, email) -> None:
    db_user = User.query.filter_by(email=email).first_or_404()

    if not bcrypt.check_password_hash(db_user.password, user.old_password):
        raise Exception("Error: incorrect old password")

    db_user.password = bcrypt.generate_password_hash(user.new_password).decode('utf-8')
    db.session.commit()
