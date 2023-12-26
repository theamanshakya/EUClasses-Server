from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Create the Flask instance
app = Flask(__name__)

# Configure your JWT settings (secret key, etc.)
app.config["JWT_SECRET_KEY"] = "your_secret_key"

# Create the JWTManager instance
jwt = JWTManager(app)

bcrypt = Bcrypt(app)
app.config.from_pyfile('config.py')  # Load configuration

db = SQLAlchemy(app)
migrate = Migrate(app, db)

CORS(app, resources={r"/*": {"origins": "*"}}) 

# Uncomment and modify the next line according to your database settings
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@host:port/database'

# Register blueprints
from main.controllers.UserController import user_blueprint
from main.controllers.CourseCategoryController import course_categories_blueprint
from main.controllers.CourseController import courses_blueprint

app.register_blueprint(user_blueprint)
app.register_blueprint(course_categories_blueprint)
app.register_blueprint(courses_blueprint)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', '*')  # Use '*' for any origin, or specify your frontend's origin
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response



