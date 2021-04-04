from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pydantic import BaseModel, constr

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    last_login_time = db.Column(db.DateTime())

    user_reviews = db.relationship('BookReview', backref='users', lazy='dynamic')

    def __repr__(self):
        return f"User('{self.id}','{self.email}', '{self.last_login_time}')"


class BookReview(db.Model):
    __tablename__ = 'book_reviews'
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    review_text = db.Column(db.String(500), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), default=1)

    def __repr__(self):
        return f"BookReview('{self.title}', '{self.review_text}','{self.category_id}', '{self.creation_date}')"


class ReviewCategory(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(50), unique=True, nullable=False)

    reviews = db.relationship('BookReview', backref='categories', lazy='dynamic')

    def __repr__(self):
        return f"ReviewCategory('{self.id}', '{self.category_name}')"


class Reaction(db.Model):
    __tablename__ = 'reactions'
    id = db.Column(db.Integer, primary_key=True)
    reacted_user = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)
    reacted_post = db.Column(db.String(50), db.ForeignKey('book_reviews.id'), nullable=False)
    reaction_type = db.Column(db.String(10), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now())

    def __repr__(self):
        return f"Reaction('{self.id}', '{self.reacted_user}', '{self.reacted_post}',\
            '{self.reaction_type}' ,'{self.creation_date}')"


class BookReviewSchema(BaseModel):
    id: int
    book: str
    title: str
    review_text: str
    category_id: int
    creation_date: datetime

    class Config:
        orm_mode = True


class ReviewCategorySchema(BaseModel):
    id: int
    category_name: str

    class Config:
        orm_mode = True
