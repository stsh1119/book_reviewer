import os
import datetime


class Config:
    JWT_SECRET_KEY = os.environ.get('DIPLOMA_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///book_reviewer.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=1)


class TestConfig:
    JWT_SECRET_KEY = 'test_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(hours=1)
