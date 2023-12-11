from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS  

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config.from_pyfile('config.py')  # Load configuration

db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app, resources={r"/*": {"origins": "*"}})

from main.controllers.UserController import user_blueprint

app.register_blueprint(user_blueprint)