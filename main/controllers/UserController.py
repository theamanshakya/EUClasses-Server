from main import db, bcrypt
from main.models.User import User
from werkzeug.security import check_password_hash
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest

class UserController:
    def register_user(self, username, email, phone, password, confirm_password, role):
        # Validate input
        if not username or not email or not phone or not password or not confirm_password:
            return {'message': 'All fields are required','code':400}, 400

        # Check if the user with the same email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_ufffser:
            return {'message': 'User with the same email already exists','code':400}, 400

        # Check if password and confirm_password match
        if password != confirm_password:
            return {'message': 'Password and confirm password do not match','code':400}, 400

        # Hash the password securely using bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Set default role if not provided
        role = role or 'student'

        # Create a new user
        new_user = User(username=username, email=email, phone=phone, password=hashed_password, role=role)
        
        try:
            db.session.add(new_user)
            db.session.commit()
            return {'message': 'User registered successfully','code':201}, 201
        except IntegrityError as e:
            db.session.rollback()
            if "duplicate key value violates unique constraint" in str(e):
                # Handle the duplicate username error here
                message = "Username already exists. Please choose a different username."
                return {'message': message, 'code': 400}, 400
            else:
                # Handle other IntegrityError cases
                print(f"Error: {e}")
                return {'message': "Registration failed due to a database error", 'code': 500}, 500
        except BadRequest as e:
            # Handle other specific exceptions if needed
            print(f"Bad request: {e}")
            return {'message': "Bad request during registration", 'code': 400}, 400
        except Exception as e:
            # Handle other generic exceptions
            db.session.rollback()
            print(f"Error: {e}")
            return {'message': "Registration failed due to an unexpected error", 'code': 500}, 500
        finally:
            # Optionally, close the database session
            db.session.close()

    def login_user(self, email, password):
        # Validate input
        if not email or not password:
            return {'message': 'Email and password are required','code':400}, 400

        # Find the user by email
        user = User.query.filter_by(email=email).first()

        if user and bcrypt.check_password_hash(user.password, password):
            # Passwords match, login successful
            return {'message': 'Login successful','code':200}, 200
        else:
            # Invalid credentials
            return {'message': 'Invalid email or password','code':401}, 401

user_blueprint = Blueprint('user_controller', __name__)
user_controller = UserController()

@user_blueprint.route('/user/register', methods=['POST'])
def register_user():
    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    role = data.get('role')

    result = user_controller.register_user(username, email, phone, password, confirm_password, role)
    return jsonify(result)

@user_blueprint.route('/user/login', methods=['POST'])
def login_user():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    result = user_controller.login_user(email, password)
    return jsonify(result)