from ..models import db, User, BookReview, BookReviewModel
from .dto import CreateReviewDto


def add_review(review: CreateReviewDto, email: str) -> None:
    user = User.query.filter_by(email=email).first_or_404()
    book_review = BookReview(book=review.book,
                             title=review.title,
                             review_text=review.review_text,
                             category=review.category,
                             user=user.id
                             )
    db.session.add(book_review)
    db.session.commit()


def all_reviews_for_book(book_name: str, page_num: int = 1) -> list:
    books = BookReview.query.filter_by(book=book_name).paginate(page=page_num, per_page=20).items
    books_list = [BookReviewModel.from_orm(book).dict() for book in books]

    return books_list
