from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    last_login_time = db.Column(db.DateTime())

    def __repr__(self):
        return f"User('{self.id}','{self.email}', '{self.last_login_time}')"


class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    review_text = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), default='Uncategorized')
    creation_date = db.Column(db.DateTime, nullable=False)
    user = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Book('{self.title}', '{self.review_text}','{self.category}', '{self.creation_date}')"


class Reaction(db.Model):
    __tablename__ = 'reactions'
    id = db.Column(db.Integer, primary_key=True)
    reacted_user = db.Column(db.String(50), db.ForeignKey('users.id'), nullable=False)
    reacted_post = db.Column(db.String(50), db.ForeignKey('books.id'), nullable=False)
    reaction_type = db.Column(db.String(50), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"Reaction('{self.id}', '{self.reacted_user}', '{self.reacted_post}',\
            '{self.reaction_type}' ,'{self.creation_date}')"
