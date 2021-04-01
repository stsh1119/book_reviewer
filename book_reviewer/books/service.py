from ..models import db, User, BookReview
from .dto import CreateReviewDto


def add_review(review: CreateReviewDto, email: str) -> None:
    user = User.query.filter_by(email=email).first_or_404()
    book_review = BookReview(title=review.title,
                             review_text=review.review_text,
                             category=review.category,
                             user=user.id
                             )
    db.session.add(book_review)
    db.session.commit()
