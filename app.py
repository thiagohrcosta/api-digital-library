import bcrypt
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models.user import User
from models.meal import Meal
from database import db
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin123@localhost:3306/digital-library'

login_manager = LoginManager()
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)


if __name__ == '__main__':
  app.run(debug=True)
