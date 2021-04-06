from ..models import (db, User, BookReview, BookReviewSchema, ReviewCategory,
                      ReviewCategorySchema, Reaction, Subscription)
from .dto import CreateReviewDto
from book_reviewer.background.tasks import send_notification_email

ITEMS_PER_PAGE = 20


def add_review(review: CreateReviewDto, email: str) -> str:
    user = User.query.filter_by(email=email).first_or_404()
    existing_categories = [category.id for category in ReviewCategory.query.all()]

    if review.category not in existing_categories:
        raise Exception("No such category: either skip this parameter, or replace it with a valid one.")

    book_review = BookReview(book=review.book,
                             title=review.title,
                             review_text=review.review_text,
                             category_id=review.category,
                             user=user.id
                             )
    db.session.add(book_review)
    db.session.commit()

    users_to_notify = Subscription.query.filter_by(subscription_category=review.category).all()
    user_emails = [user.user_email for user in users_to_notify]

    if user_emails:
        category_name = ReviewCategory.query.filter_by(id=review.category).first().category_name
        send_notification_email.delay(users_list=user_emails, review_category=category_name)
        return 'Book review was added'

    return 'Book review was added'


def all_reviews_for_book(book_name: str, page_number: int = 1) -> list:
    books = BookReview.query.filter_by(book=book_name).paginate(page=page_number,
                                                                per_page=ITEMS_PER_PAGE,
                                                                error_out=False
                                                                ).items
    books_list = [BookReviewSchema.from_orm(book).dict() for book in books]

    return books_list


def all_reviews_for_all_books(page_number: int = 1) -> list:
    books = BookReview.query.paginate(page=page_number, per_page=ITEMS_PER_PAGE, error_out=False).items
    books_list = [BookReviewSchema.from_orm(book).dict() for book in books]

    return books_list


def all_categories_for_books() -> list:
    categories = ReviewCategory.query.all()
    category_names_list = [ReviewCategorySchema.from_orm(category).dict() for category in categories]

    return category_names_list


def all_reviews_under_certain_category(category_name: str, page_number: int = 1) -> list:
    needed_category = ReviewCategory.query.filter_by(category_name=category_name).first_or_404()
    reviews = needed_category.reviews.paginate(page=page_number, per_page=ITEMS_PER_PAGE).items

    reviews_under_category = [BookReviewSchema.from_orm(review).dict() for review in reviews]

    return reviews_under_category


def all_reviews_made_by_user(user_email: str, page_number: int = 1) -> list:
    user = User.query.filter_by(email=user_email).first_or_404()
    reviews_made_by_user = user.user_reviews.paginate(page=page_number,
                                                      per_page=ITEMS_PER_PAGE,
                                                      error_out=False).items

    serialized_reviews = [BookReviewSchema.from_orm(review).dict() for review in reviews_made_by_user]

    return serialized_reviews


def like_review(review_id: int, user_email: str) -> str:
    review = BookReview.query.filter_by(id=review_id).first_or_404()
    user_id = User.query.filter_by(email=user_email).first().id

    reaction_exists = Reaction.query.filter_by(reacted_post=review.id, reacted_user=user_id).first()
    if not reaction_exists:
        reaction = Reaction(reacted_user=user_id,
                            reacted_post=review.id,
                            reaction_type='like',
                            )
        db.session.add(reaction)
        db.session.commit()
        return 'Post was liked.'

    return 'You have already liked this post.'


def unlike_review(review_id: int, user_email: str) -> str:
    user_id = User.query.filter_by(email=user_email).first().id
    reaction = Reaction.query.filter_by(reacted_post=review_id, reacted_user=user_id).first()

    if reaction:
        db.session.delete(reaction)
        db.session.commit()
        return 'Your reaction was removed.'

    return 'You have not reacted to this post.'


def sign_up_for_email_notifications(category_id: int, email: str) -> str:
    category = ReviewCategory.query.filter_by(id=category_id).first_or_404()
    is_already_subscribed = Subscription.query.filter_by(user_email=email,
                                                         subscription_category=category.id
                                                         ).first()
    if not is_already_subscribed:
        subscription = Subscription(user_email=email,
                                    subscription_category=category.id)
        db.session.add(subscription)
        db.session.commit()
        return f'{email} has signed up for {category.category_name}.'

    return f'{email} is already signed up for {category.category_name}.'


def unsubscribe_from_email_notifications(category_id: int, email: str) -> str:
    subscription = Subscription.query.filter_by(user_email=email,
                                                subscription_category=category_id
                                                ).first()
    if subscription:
        db.session.delete(subscription)
        db.session.commit()
        return f'{email} cancelled subscription for {subscription.subscription_category}.'

    return f'{email} is not subscribed for {category_id}.'


def view_my_subscriptions(email: str) -> [list, str]:
    subscriptions = Subscription.query.filter_by(user_email=email).all()
    if subscriptions:
        subscriptions_list = [subscriptions.subscription_category for subscriptions in subscriptions]
        return subscriptions_list
    return f'{email} does not have any subscriptions'
