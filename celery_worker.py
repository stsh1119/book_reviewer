from book_reviewer import create_app
from book_reviewer.background.celery_creator import celery
from book_reviewer.background.celery_utils import init_celery

app = create_app()
init_celery(celery, app)
