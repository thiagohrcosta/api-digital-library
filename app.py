import bcrypt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models.user import User
from models.book import Book
from models.author import Author
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@localhost:3306/api-digital-library'

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

  if not author:
    return jsonify({'message': 'Author not found.'})
  
  author.name = data.get('name')
  author.photo = data.get('photo')
  db.session.commit()

  return jsonify({'message': f"{author.name} successfully updated."})

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

if __name__ == '__main__':
  app.run(debug=True)
