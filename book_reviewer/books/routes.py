from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from book_reviewer.utils import json_body_required
from .dto import CreateReviewDto
from .service import (add_review, all_reviews_for_book, all_reviews_for_all_books, all_categories_for_books,
                      all_reviews_under_certain_category, all_reviews_made_by_user, like_review, unlike_review,
                      sign_up_for_email_notifications, unsubscribe_from_email_notifications, view_my_subscriptions)


books = Blueprint('books', __name__)


@books.route('/add_review', methods=['POST'])
@json_body_required
@jwt_required()
def add_new_review():
    try:
        review_creation_data = CreateReviewDto.parse_obj(request.json)
        result = add_review(review_creation_data, email=get_jwt_identity())
        return jsonify(result), 201

    except ValidationError as e:
        return e.json(), 400

    except Exception as e:
        return jsonify(str(e)), 400


@books.route("/reviews/<string:book>", methods=['GET'])
@jwt_required(optional=True)
def view_all_reviews_for_a_book(book):
    page_num = int(request.args.get('page', default=1))
    result = all_reviews_for_book(book_name=book, page_number=page_num)

    return jsonify(result), 200


@books.route("/reviews/all", methods=['GET'])
@jwt_required(optional=True)
def view_all_reviews_for_all_books():
    page_num: int = int(request.args.get('page', default=1))
    result = all_reviews_for_all_books(page_num)

    return jsonify(result), 200


@books.route("/categories", methods=['GET'])
@jwt_required(optional=True)
def view_all_categories_for_books():
    result = all_categories_for_books()
    return jsonify(result), 200


@books.route("/categories/<string:category_name>", methods=['GET'])
@jwt_required(optional=True)
def view_all_reviews_under_given_category(category_name):
    page_num = int(request.args.get('page', default=1))
    result = all_reviews_under_certain_category(category_name, page_num)

    return jsonify(result), 200


@books.route("/<string:user>/reviews", methods=['GET'])
@jwt_required(optional=True)
def view_all_reviews_under_user(user):
    page_num = int(request.args.get('page', default=1))
    result = all_reviews_made_by_user(user, page_num)

    return jsonify(result), 200


@books.route("/my_reviews", methods=['GET'])
@jwt_required()
def view_reviews_under_current_user():
    page_num = int(request.args.get('page', default=1))
    result = all_reviews_made_by_user(get_jwt_identity(), page_num)

    return jsonify(result), 200


@books.route("/reviews/<int:review_id>/like", methods=['POST'])
@jwt_required()
def like_a_review(review_id):
    result = like_review(review_id, get_jwt_identity())
    return jsonify(result), 200


@books.route("/reviews/<int:review_id>/unlike", methods=['DELETE'])
@jwt_required()
def unlike_a_review(review_id):
    result = unlike_review(review_id, get_jwt_identity())
    return jsonify(result), 200


@books.route("/sign_up/<int:category_id>", methods=['POST'])
@jwt_required()
def sign_up_for_notifications(category_id):
    return jsonify(sign_up_for_email_notifications(category_id, get_jwt_identity())), 200


@books.route("/remove_subscription/<int:category_id>", methods=['DELETE'])
@jwt_required()
def remove_email_notifications(category_id):
    return jsonify(unsubscribe_from_email_notifications(category_id, get_jwt_identity())), 200


@books.route("/view_subscriptions", methods=['GET'])
@jwt_required()
def view_subscriptions():
    return jsonify(view_my_subscriptions(get_jwt_identity())), 200
