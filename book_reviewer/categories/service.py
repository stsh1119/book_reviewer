from ..models import BookReviewSchema, ReviewCategory, ReviewCategorySchema

ITEMS_PER_PAGE = 20


def all_categories_for_books() -> list:
    """Returns all category names and ids"""
    categories = ReviewCategory.query.all()
    category_names_list = [ReviewCategorySchema.from_orm(category).dict() for category in categories]

    return category_names_list


def all_reviews_under_certain_category(category_id: int, page_number: int = 1) -> list:
    """Returns all book reviews under given category_id"""
    needed_category = ReviewCategory.query.filter_by(id=category_id).first_or_404()
    reviews = needed_category.reviews.paginate(page=page_number, per_page=ITEMS_PER_PAGE).items

    reviews_under_category = [BookReviewSchema.from_orm(review).dict() for review in reviews]

    return reviews_under_category
