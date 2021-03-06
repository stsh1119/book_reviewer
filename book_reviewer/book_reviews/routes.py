from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from book_reviewer.utils import json_body_required
from .dto import CreateReviewDto
from .service import (add_review, all_reviews_for_book, all_reviews_for_all_books, all_reviews_made_by_user,
                      like_review, unlike_review, sign_up_for_email_notifications,
                      unsubscribe_from_email_notifications, view_my_subscriptions)


book_reviews = Blueprint('book_reviews', __name__)


@book_reviews.post('/add_review')
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


@book_reviews.get("/reviews/<string:book>")
@jwt_required(optional=True)
def view_all_reviews_for_a_book(book):
    page_num = int(request.args.get('page', default=1))
    result = all_reviews_for_book(book_name=book, page_number=page_num)

    return jsonify(result), 200


@book_reviews.get("/reviews/all")
@jwt_required(optional=True)
def view_all_reviews_for_all_books():
    page_num: int = int(request.args.get('page', default=1))
    result = all_reviews_for_all_books(page_num)

    return jsonify(result), 200


@book_reviews.get("/<string:user>/reviews")
@jwt_required(optional=True)
def view_all_reviews_under_user(user):
    page_num = int(request.args.get('page', default=1))
    result = all_reviews_made_by_user(user, page_num)

    return jsonify(result), 200


@book_reviews.get("/my_reviews")
@jwt_required()
def view_reviews_under_current_user():
    page_num = int(request.args.get('page', default=1))
    result = all_reviews_made_by_user(get_jwt_identity(), page_num)

    return jsonify(result), 200


@book_reviews.post("/reviews/<int:review_id>/like")
@jwt_required()
def like_a_review(review_id):
    result = like_review(review_id, get_jwt_identity())
    return jsonify(result), 200


@book_reviews.delete("/reviews/<int:review_id>/unlike")
@jwt_required()
def unlike_a_review(review_id):
    result = unlike_review(review_id, get_jwt_identity())
    return jsonify(result), 200


@book_reviews.post("/sign_up/<int:category_id>")
@jwt_required()
def sign_up_for_notifications(category_id):
    return jsonify(sign_up_for_email_notifications(category_id, get_jwt_identity())), 200


@book_reviews.delete("/remove_subscription/<int:category_id>")
@jwt_required()
def remove_email_notifications(category_id):
    return jsonify(unsubscribe_from_email_notifications(category_id, get_jwt_identity())), 200


@book_reviews.get("/view_subscriptions")
@jwt_required()
def view_subscriptions():
    return jsonify(view_my_subscriptions(get_jwt_identity())), 200
