from database import db

class Book(db.Model):
  id = db.Column(db.Integer, unique=True, primary_key=True)
  title = db.Column(db.String(255), nullable=False)
  
  author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    