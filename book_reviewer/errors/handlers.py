from flask import Blueprint, jsonify

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    return jsonify('Could not find what you are looking for'), 404


@errors.app_errorhandler(405)
def error_405(error):
    return jsonify('The method is not allowed for the requested endpoint'), 405


@errors.app_errorhandler(500)
def error_500(error):
    return jsonify('Server error happened'), 500
