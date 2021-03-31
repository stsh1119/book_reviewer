from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, create_access_token, jwt_required
from pydantic import ValidationError
from .dto import UserRegisterDto, UserLoginDto
from .service import register_user, login_user

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=["POST"])
def register():
    if not request.json:
        return jsonify(message='Missing request body'), 400

    try:
        user = UserRegisterDto.parse_obj(request.json)
        register_user(user)
        return jsonify(message='Successfully registered.'), 201
    except ValidationError as e:
        return e.json(), 400
    except Exception as e:
        return jsonify(message=str(e)), 400


@auth.route("/login", methods=["POST"])
def login():
    try:
        user_data = UserLoginDto.parse_obj(request.json)
        tokens = login_user(user_data)
        return jsonify(tokens), 200
    except ValidationError as e:
        return e.json(), 400
    except Exception as e:
        return jsonify(message=str(e)), 400


@auth.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), 200
