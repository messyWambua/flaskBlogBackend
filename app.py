from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
wsgi_app = app.wsgi_app
app.config['SECRET_KEY'] = 'continue_Guessing'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///TestDb.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
# used to show where function for login required leads to
login_manager.login_message_category = 'info'

from routes import *

if __name__ == '__main__':
    app.run(debug=1)
 