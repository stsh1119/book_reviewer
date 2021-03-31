from flask import Blueprint, jsonify

books = Blueprint('books', __name__)


@books.route('/')
def home():
    return jsonify('hello')
