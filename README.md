# Book_reviewer
Made as a diploma project for Sumy State University.

## 🛠 Tech stack
I tried to keep things as simple, as possible, so used the following stack: **Flask, SQLAlchemy, Redis, Celery**

Amongst other libraries, that were used: bcrypt, pydantic, Flask-JWT-Extended, loguru

##  Installing and running locally


1. Install [Redis](https://redis.io/download)

2. Clone the repo, create venv and install dependencies
   
    ```shell
    $ git clone https://github.com/stsh1119/book_reviewer.git
    $ cd book_reviewer
    $ python -m venv venv
    $ source venv/bin/activate
    $ pip install -r requirements.txt
    ```

3. Run Redis and Celery

    ```shell
    $ redis-server
    $ celery -A celery_worker.celery worker --loglevel=info --pool=solo
    ```

This will start the application in development mode on [http://127.0.0.1:5000/](http://127.0.0.1:5000/), as well as other necessary services: sqlite database, redis and queue with workers.

## How to use endpoints:

1. To register, send a POST request to `/register` with the following body:
```json
{
	"email": "stanislav_shulhah@gmail.com",
	"password": "1234",
	"confirm_password": 1234
}
```

2. To login send a POST request to `/login` with the following body:
```json
{
	"email": "stanislav_shulhah@gmail.com",
	"password": "1234"
}
```

3. To get a new access token, send a request to `/refresh` with a refresh token in header

4. To change password send a POST request to `/change_password` with the following body:
```json
{
	"old_password": "1233",
	"new_password": "1234",
	"confirm_new_password": "1234"
}
```
**!NB** Validation will fail in case new password is the same as an old or if new_password and confirm_new_password are different

5. To view all review categories send a GET request to `/categories`:

6. To view all review under specific category send a GET request to `/categories/<category_id>`:

7. To view all reviews send a GET request to `/reviews/all`, pagination is accessible using `?page=2`

8. When logged in, view all reviews made by you by sending a GET request to `/my_reviews`

9. To view all reviews made by another user send a GET request to `/<email>/reviews?page=1`
   
10. To view all reviews for certain book, send a GET request to `/reviews/Automate the boring stuff?page=1`
 
11. To like a review send a POST request to `reviews/<review_id>/like`

12. To unlike a review send a DELETE request to `reviews/<review_id>/unlike`

13. To add a review send a POST request to `/add_review` with the following body structure, 
in case `category_id` is omitted, book review will be marked as 'Uncategorized'
```json
{
	"book": "Web development with Flask",
	"title": "Perfect book for beginners",
	"review_text": "The book itself if very very good...",
	"category_id": 6
}
```

14. To sign up for email notifications whenever new review is added under certain category, send a POST request `/sign_up/<category_id>`

15. To view current subscriptions send GET request to `/view_subscriptions`

14. To stop receiving email notifications whenever new review is added under certain category, send a DELETE request `/remove_subscription/<category_id>`
