from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from book_reviewer.utils import json_body_required
from .dto import CreateReviewDto
from .service import add_review, all_reviews_for_book

books = Blueprint('books', __name__)


@books.route('/add_review', methods=['POST'])
@json_body_required
@jwt_required()
def add_new_review():
    try:
        review_creation_data = CreateReviewDto.parse_obj(request.json)
        add_review(review_creation_data, email=get_jwt_identity())
        return jsonify('Book review was added'), 201
    except ValidationError as e:
        return e.json(), 400


@books.route("/reviews/<string:book>", methods=['GET'])
def view_all_reviews_for_a_book(book):
    result = all_reviews_for_book(book_name=book, page_num=int(request.args.get('page')))
    return jsonify(result), 200
