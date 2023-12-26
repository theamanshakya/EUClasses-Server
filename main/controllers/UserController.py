from flask import Blueprint, request, jsonify
from sqlalchemy import exc
from main import db, bcrypt
from main.models.User import User,TokenBlocklist
from flask_jwt_extended import jwt_required,create_access_token,create_refresh_token,get_jwt_identity,get_jwt
from main import app
from datetime import datetime, timezone

class UserController:
    def _validate_registration(self, username, email, phone, password, role):
        errors = {}
    
    def get_all_students(self):
        students = User.query.filter_by(role='student').all()
        student_data : any = [{
            "id" : user.id,
            "username" : user.username,
            "email" : user.email,
            "phone" : user.phone,
            "role" : user.role
        } for user in students]  # Convert to dictionaries
        print(student_data)
        return student_data

    def get_student_by_id(student_id):
        return User.query.filter_by(id=student_id, role='student').first()

    def create_student(data):
        student = User(**data)  # Assuming data is a dictionary with relevant fields
        db.session.add(student)
        db.session.commit()
        return student

    def update_student(student_id, data):
        student = User.query.filter_by(id=student_id, role='student').first()
        if student:
            for key, value in data.items():
                setattr(student, key, value)
            db.session.commit()
            return student
        else:
            return None  # Or raise an exception if student not found

    def delete_student(student_id):
        student = User.query.filter_by(id=student_id, role='student').first()
        if student:
            db.session.delete(student)
            db.session.commit()
            return True
        else:
            return False  # Or raise an exception if student not found

    def register_user(self, data):
        errors = self._validate_registration(**data)
        if errors:
            return {"message": "Registration failed", "errors": errors}, 400

        try:
            new_user = User(**data)
            new_user.password = bcrypt.generate_password_hash(data["password"]).decode("utf-8")
            db.session.add(new_user)
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            if "duplicate key value violates unique constraint" in str(e):
                return {"message": "Username already exists", "error": "duplicate_username"}, 400
            return {"message": "Registration failed due to a database error"}, 500
        except Exception as e:
            db.session.rollback()
            return {"message": "Registration failed due to an unexpected error"}, 500
        finally:
            db.session.close()

        return {"message": "User registered successfully"}, 201

    def login_user(self, data):
        if not all([data.get("email"), data.get("password")]):
            return {"message": "Email and password are required"}, 400

        user = User.query.filter_by(email=data.get("email")).first()
        if not user or not bcrypt.check_password_hash(user.password, data["password"]):
            return {"message": "Invalid email or password"}, 401

        # Generate access and refresh tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        # Create session for user
        # TODO: Implement session logic based on your chosen library (e.g., Flask-Session)

        # Prepare response data
        response_data = {"message": "Login successful", "user": user.serialize()}
        response_data["access_token"] = access_token
        response_data["refresh_token"] = refresh_token

        return {"data": response_data}, 200
    @jwt_required()
    def logout_user(self):
        # Revoke the current user's access token
        # print("Received request headers:", request.headers)

        try:
            jti = get_jwt()["jti"]
            now = datetime.now(timezone.utc)
            db.session.add(TokenBlocklist(jti=jti, created_at=now))
            db.session.commit()
            # return jsonify(msg="JWT revoked")
            return jsonify({"message": "Successfully logged out"}), 200

        except KeyError:
            return jsonify({"message": "Access token not found"}), 500

    @jwt_required()
    def get_logged_in_user(self):
        # Get the user ID from the JWT payload
        user_id = get_jwt_identity()

        # Fetch user details from database
        user = User.query.get(user_id)

        # Check if user exists
        if not user:
            return jsonify({"message": "User not found"}), 404

        # Return user details
        return jsonify({"user": user.serialize()}), 200


user_blueprint = Blueprint("user_controller", __name__)
user_controller = UserController()

@user_blueprint.route("/", methods=['GET'])
def register_new_user():
    return "<h1>Hello</h1>"

@user_blueprint.route("/user/register", methods=["POST"])
def register_user():
    data = request.get_json()
    result = user_controller.register_user(data)
    return jsonify(result)

@user_blueprint.route("/user/login", methods=["POST"])
def login_user():
    data = request.get_json()
    result = user_controller.login_user(data)
    return jsonify(result)

@user_blueprint.route("/user/logout", methods=["POST"])
def logout_user():
    result = user_controller.logout_user()
    return result

@user_blueprint.route("/user/details", methods=["GET"])
def get_logged_in_user():
    result = user_controller.get_logged_in_user()
    return result

@user_blueprint.route("/user/students/all", methods=["GET"])
def get_all_student_data():
    result = user_controller.get_all_students()
    return jsonify(result)