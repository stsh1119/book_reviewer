from functools import wraps
from flask import request, jsonify, abort, make_response


def json_body_required(original_function):
    @wraps(original_function)
    def wrapper(*args, **kwargs):
        if not request.json:
            abort(make_response(jsonify(message="Missing request body"), 400))
        return original_function(*args, **kwargs)
    return wrapper
