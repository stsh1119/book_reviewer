from ..models import db, User, BookReview, BookReviewSchema, ReviewCategory, Reaction, Subscription
from .dto import CreateReviewDto
from book_reviewer.background.tasks import send_notification_email

ITEMS_PER_PAGE = 20


def add_review(review: CreateReviewDto, email: str) -> str:
    """Adds a new book review, calls background function in case there are users to be notified"""
    user = User.query.filter_by(email=email).first_or_404()
    existing_categories = {review.id: review.category_name for review in ReviewCategory.query.all()}

    if review.category_id not in existing_categories.keys():
        raise Exception("No such category: either skip this parameter, or replace it with a valid one.")

    book_review = BookReview(
        book=review.book,
        title=review.title,
        review_text=review.review_text,
        category_id=review.category_id,
        user=user.id
    )
    db.session.add(book_review)
    db.session.commit()

    users_to_notify = Subscription.query.filter_by(subscription_category=review.category_id).all()
    user_emails = [user.user_email for user in users_to_notify]

    if user_emails:
        send_notification_email.delay(users_list=user_emails, review_category=existing_categories[review.category_id])
        return 'Book review was added'

    return 'Book review was added'


def all_reviews_for_book(book_name: str, page_number: int = 1) -> list:
    """Returns all reviews for a given book name, ordered by creation date descending"""
    books = BookReview.query.filter_by(book=book_name).order_by(BookReview.creation_date.desc()).paginate(
        page=page_number,
        per_page=ITEMS_PER_PAGE,
        error_out=False).items
    books_list = [BookReviewSchema.from_orm(book).dict() for book in books]

    return books_list


def all_reviews_for_all_books(page_number: int = 1) -> list:
    """Returns all reviews for all books, ordered by creation date descending"""
    books = BookReview.query.order_by(BookReview.creation_date.desc())
    paginated_books = books.paginate(page=page_number, per_page=ITEMS_PER_PAGE, error_out=False)
    serialized_books_list = [BookReviewSchema.from_orm(book).dict() for book in paginated_books.items]

    return serialized_books_list


def all_reviews_made_by_user(user_email: str, page_number: int = 1) -> list:
    """Returns all reviews made by certain user"""
    user = User.query.filter_by(email=user_email).first_or_404()
    reviews_made_by_user = user.user_reviews.paginate(page=page_number, per_page=ITEMS_PER_PAGE, error_out=False).items

    serialized_reviews = [BookReviewSchema.from_orm(review).dict() for review in reviews_made_by_user]

    return serialized_reviews


def like_review(review_id: int, user_email: str) -> str:
    """Marks review as 'liked' for certain user"""
    review = BookReview.query.filter_by(id=review_id).first_or_404()
    user_id = User.query.filter_by(email=user_email).first().id

    reaction_exists = Reaction.query.filter_by(reacted_post=review.id, reacted_user=user_id).first()

    if not reaction_exists:
        reaction = Reaction(reacted_user=user_id, reacted_post=review.id, reaction_type='like', )
        db.session.add(reaction)
        db.session.commit()
        return 'Post was liked.'

    return 'You have already liked this post.'


def unlike_review(review_id: int, user_email: str) -> str:
    """Removes 'like' reaction from a review"""
    user_id = User.query.filter_by(email=user_email).first().id
    reaction = Reaction.query.filter_by(reacted_post=review_id, reacted_user=user_id).first()

    if reaction:
        db.session.delete(reaction)
        db.session.commit()
        return 'Your reaction was removed.'

    return 'You have not reacted to this post.'


def sign_up_for_email_notifications(category_id: int, email: str) -> str:
    """
    Adds user to the list of subscribers under a certain category of reviews,
    so that user gets an email notification whenever review is added"""
    category = ReviewCategory.query.filter_by(id=category_id).first_or_404()
    is_already_subscribed = Subscription.query.filter_by(user_email=email, subscription_category=category.id).first()

    if not is_already_subscribed:
        subscription = Subscription(user_email=email, subscription_category=category.id)
        db.session.add(subscription)
        db.session.commit()
        return f'{email} has signed up for {category.category_name}.'

    return f'{email} is already signed up for {category.category_name}.'


def unsubscribe_from_email_notifications(category_id: int, email: str) -> str:
    """Removes users subscription for a given category"""
    subscription = Subscription.query.filter_by(user_email=email, subscription_category=category_id).first()
    if subscription:
        db.session.delete(subscription)
        db.session.commit()
        return f'{email} cancelled subscription for {subscription.subscription_category}.'

    return f'{email} is not subscribed for {category_id}.'


def view_my_subscriptions(email: str) -> [list, str]:
    """Lists all subscriptions under given user, if there are any"""
    subscriptions = Subscription.query.filter_by(user_email=email).all()
    if subscriptions:
        subscriptions_list = [subscriptions.subscription_category for subscriptions in subscriptions]
        return subscriptions_list

    return f'{email} does not have any subscriptions'
