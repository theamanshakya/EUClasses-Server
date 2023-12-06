from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_pyfile('config.py')  # Load configuration

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app.models import User

from app.routes import main_routes
