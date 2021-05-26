# Book_reviewer
Made as a diploma project for Sumy State University.

## 🛠 Tech stack
I tried to keep things as simple, as possible, so used the following stack: **Flask, SQLAlchemy, Redis, Celery**

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
