from database import db
from flask_login import UserMixin

user_books = db.Table('user_books',
  db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
  db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
)

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, unique=True, primary_key=True)
  email = db.Column(db.String(80), unique=True, nullable=False)
  username = db.Column(db.String(32), unique=True, nullable=False)
  password = db.Column(db.String(80), nullable=False)
  role = db.Column(db.String(8), nullable=False, default='user')

  books = db.relationship('Book', secondary=user_books, backref=db.backref('users', lazy='dynamic'))
