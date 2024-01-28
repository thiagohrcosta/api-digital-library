import bcrypt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models.user import User
from models.book import Book
from models.author import Author
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@localhost:3306/api-digital-library'
CORS(app)

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@app.route('/user', methods=['POST'])
def create_user():
  data = request.json
  username = data.get('username')
  password = data.get('password')
  email = data.get('email')

  if username and password: 
    hashed_password = bcrypt.hashpw(str.encode(password), bcrypt.gensalt())
    user = User(username=username, email=email, password=hashed_password, role='user')
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User successfully created.'})

  return jsonify({'message': 'Invalid data'}), 400

# Login User
@app.route('/login', methods=['POST'])
def login():
  data = request.json
  username = data.get('username')
  password = data.get('password')

  if username and password:
    user = User.query.filter_by(username=username).first()

    if user and bcrypt.checkpw(str.encode(password), str.encode(user.password)):
      login_user(user)
      print(current_user.is_authenticated)
      return jsonify({'message': 'The user signed in successfully.'})
    
  return jsonify({'message': 'Invalid credentials'}), 400

# Logout user
@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return jsonify({'message': 'User logout successfully'})

# AUTHOR

# AUTHORS
@app.route('/authors', methods=['GET'])
def authors():
  authors = Author.query.all()

  if len(authors) == 0:
    return jsonify({'message': "No authors on database"}), 404

  authors_data = [{
    'id': author.id,
    'name': author.name,
    'photo': author.photo
  } for author in authors]

  return jsonify(authors_data)

# AUTHOR
@app.route('/authors/<int:id_author>', methods=['GET'])
def author(id_author):
  author = Author.query.get(id_author)

  if author:
    return jsonify({
      'name': author.name,
      'photo': author.photo
    })
  
  return jsonify({'message': 'Author not found'}), 400

# CREATE AUTHOR
@app.route('/authors', methods=['POST'])
@login_required
def create_author():
  if current_user.role != 'admin':
    return jsonify({'message': 'Action not allowed'}), 403
  
  data = request.json
  name = data.get('name')
  photo = data.get('photo')
  
  if name and photo:
    author = Author(name=name, photo=photo)

    author_exists = Author.query.filter_by(name=name).first()

    if author_exists:
      return jsonify({'message': f"{author_exists.name} already exists on database."})
    
    db.session.add(author)
    db.session.commit()

    return jsonify({'message': f'{name} was successfully added to the database.'})
  
# UPDATE AUTHOR
@app.route('/authors/<int:id_author>', methods=['PATCH'])
@login_required
def edit_author(id_author):
  if current_user.role != 'admin':
    return jsonify({'message': 'Action not allowed'}), 403

  data = request.json
  author = Author.query.get(id_author)

  if author:
    author.name = data.get('name')
    author.photo = data.get('photo')
    db.session.commit()

    return jsonify({'message': f"{author.name} successfully updated."})

  return jsonify({'message': 'Author not found.'})
  
# DELETE AUTHOR
@app.route('/authors/<int:id_author>', methods=['DELETE'])
@login_required
def delete_author(id_author):
  if current_user.role != 'admin':
    return jsonify({'message': 'Action not allowed'}), 403
  
  author = Author.query.get(id_author)

  if not author:
    return jsonify({'message': "Author not found."})
  
  db.session.delete(author)
  db.session.commit()

  return jsonify({"message": "Author successfully deleted."})

# BOOK

# BOOK INDEX
@app.route('/books', methods=['GET'])
def books():
  books = Book.query.all()

  if len(books) > 0:
    books_data = [{
      'id': book.id,
      'title': book.title,
      'box_cover': book.box_cover,
      'author': Author.query.filter_by(id=book.author_id).first().name
    } for book in books]

    return jsonify(books_data)
  
  return jsonify({'message': 'No book found on database.'})

# SHOW BOOK
@app.route('/books/<int:id_book>', methods=['GET'])
def book(id_book):
  book = Book.query.get(id_book)

  author = Author.query.filter_by(id=book.author_id).first()
  author_name = author.name

  if book:
    author = Author.query.filter_by(id=book.author_id).first()
    author_name = author.name if author else "Unknown Author"

    return jsonify({
      'id': book.id,
      'title': book.title,
      'box_cover': book.box_cover,
      'author': author_name
    })

  return jsonify({'message': "Book not found"}), 404

# CREATE BOOK
@app.route('/books', methods=['POST'])
@login_required
def create_book():
  if current_user.role != 'admin':
    return jsonify({'message': 'Action not allowed'}), 403
  
  data = request.json
  title = data.get('title')
  box_cover = data.get('box_cover')
  author_id = data.get('author_id')

  existing_book = Book.query.filter_by(title=title).first()
  if existing_book:
      return jsonify({'message': 'A book with the same title already exists'}), 400

  if title and box_cover and author_id:
    book = Book(title=title, box_cover=box_cover, author_id=author_id)
    db.session.add(book)
    db.session.commit()

    return jsonify({'message': 'Book successfully created.'})
  
  return jsonify({'message': 'Invalid data'}), 400

# UPDATE BOOK
@app.route('/books/<int:id_book>', methods=['PATCH'])
@login_required
def update_book(id_book):
  if current_user.role != 'admin':
    return jsonify({'message': 'Action not allowed'}), 403

  data = request.json
  book = Book.query.get(id_book)

  if book:
    book.title = data.get('title')
    book.box_cover = data.get('box_cover')
    book.author_id = data.get('author_id')
    db.session.commit()

    return jsonify({'message': f"{book.title} successfully updated."})

  return jsonify({'message': 'Author not found.'})

# DELETE BOOK
@app.route('/books/<int:id_book>', methods=['DELETE'])
@login_required
def delete_book(id_book):
  if current_user.role != 'admin':
    return jsonify({'message': 'Action not allowed'}), 403
  
  book = Book.query.get(id_book)

  if book:
    db.session.delete(book)
    db.session.commit()

    return jsonify({'message': 'Book successfully deleted.'})

  return jsonify({'message': 'Book not found'}), 400

# BOOKSHELF
@app.route('/add_book/<int:id_book>', methods=['POST'])
def add_to_bookshelf(id_book):
  user = current_user

  book = Book.query.get(id_book)

  if not book:
    return jsonify({'message': 'Book not found'}), 404

  if book in user.books:
    return jsonify({'message': 'Book already in your collection'}), 400

  user.books.append(book)
  db.session.commit()

  return jsonify({'message': 'Book successfully added to your collection'})

@app.route('/profile/<int:id_user>', methods=['GET'])
def profile(id_user):
  user = User.query.get(id_user)

  if user:
    user_data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'books': [{'id': book.id, 'title': book.title, 'box_cover': book.box_cover} for book in user.books]
    }

    return jsonify(user_data)
  
  return jsonify({'message': 'User not found'}), 404


if __name__ == '__main__':
  app.run(debug=True)
