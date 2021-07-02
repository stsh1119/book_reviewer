from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from .service import all_categories_for_books, all_reviews_under_certain_category


categories = Blueprint('categories', __name__)


@categories.get("/categories")
@jwt_required(optional=True)
def view_all_categories_for_books():
    result = all_categories_for_books()
    return jsonify(result), 200


@categories.get("/categories/<int:category_id>")
@jwt_required(optional=True)
def view_all_reviews_under_given_category(category_id):
    page_num = int(request.args.get('page', default=1))
    result = all_reviews_under_certain_category(category_id, page_num)

    return jsonify(result), 200
