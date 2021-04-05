from book_reviewer import create_app
from book_reviewer.celery_creator import celery

if __name__ == "__main__":
    app = create_app(celery=celery)
    app.run(debug=True)
