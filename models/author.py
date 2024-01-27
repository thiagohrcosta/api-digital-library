from database import db

class Author(db.Model):
  id = db.Column(db.Integer, unique=True, primary_key=True)
  name = db.Column(db.String(64), nullable=False)

  books = db.relationship('Book', backref='author', lazy=True)
