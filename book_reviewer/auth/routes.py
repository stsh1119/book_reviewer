from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required
from pydantic import ValidationError
from .dto import UserRegisterDto, UserLoginDto, UserChangePwdDto
from .service import register_user, login_user, change_pwd
from book_reviewer.utils import json_body_required

auth = Blueprint('auth', __name__)


@auth.post('/register')
@json_body_required
def register():
    try:
        user = UserRegisterDto.parse_obj(request.json)
        register_user(user)
        return jsonify(message='Successfully registered.'), 201

    except ValidationError as e:
        return e.json(), 400

    except Exception as e:
        return jsonify(message=str(e)), 400


@auth.post("/login")
@json_body_required
def login():
    try:
        user_data = UserLoginDto.parse_obj(request.json)
        tokens = login_user(user_data)
        return jsonify(tokens), 200

    except ValidationError as e:
        return e.json(), 400

    except Exception as e:
        return jsonify(message=str(e)), 400


@auth.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), 200


@auth.post("/change_password")
@jwt_required()
@json_body_required
def change_password():
    try:
        user_data = UserChangePwdDto.parse_obj(request.json)
        change_pwd(user_data, email=get_jwt_identity())
        return jsonify(message='Password was changed'), 200

    except ValidationError as e:
        return e.json(), 400

    except Exception as e:
        return jsonify(str(e)), 400
