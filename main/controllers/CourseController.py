from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from main import app, db
from main.models.Course import Course  # Adjust the import according to your project structure

courses_blueprint = Blueprint('courses', __name__)

@courses_blueprint.route('/courses', methods=['GET'])
def get_courses():
    print("called")
    courses = Course.query.all()
    return jsonify({'courses': [course.to_dict() for course in courses]})

@courses_blueprint.route('/courses/<int:course_id>', methods=['GET'])
def get_course(course_id):
    course = Course.query.get(course_id)
    if course:
        return jsonify({'course': course.to_dict()})
    else:
        return jsonify({'message': 'Course not found'}), 404

@courses_blueprint.route('/courses', methods=['POST'])
def create_course():
    data = request.form
    # write a for loop
    for x in data:
        print(x)

    print(request.form)
    thumbnail = request.files['file']

    if thumbnail and allowed_file(thumbnail.filename):
        filename = secure_filename(thumbnail.filename)
        thumbnail.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        thumbnail_url = f"/static/img/{filename}"
    else:
        return jsonify({'error':'Invalid file or no file part'}), 400

    try:
        new_course = Course(
            title=data['title'],
            category=data['category'],
            language=data['language'],
            duration=data['duration'],
            description=data['description'],
            thumbnail=thumbnail_url,
            price=float(data['price'])
        )
        db.session.add(new_course)
        db.session.commit()
        return jsonify({'message': 'Course created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create course: ' + str(e)}), 500

@courses_blueprint.route('/courses/<int:course_id>', methods=['PUT'])
def update_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Course not found'}), 404

    data = request.form
    if 'thumbnail' in request.files:
        thumbnail = request.files['thumbnail']
        if thumbnail and allowed_file(thumbnail.filename):
            filename = secure_filename(thumbnail.filename)
            thumbnail.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            course.thumbnail = f"/static/img/{filename}"

    course.title = data.get('title', course.title)
    course.category = data.get('category', course.category)
    course.language = data.get('language', course.language)
    course.duration = data.get('duration', course.duration)
    course.description = data.get('description', course.description)
    course.price = float(data.get('price', course.price))

    db.session.commit()
    return jsonify({'message': 'Course updated successfully'})

@courses_blueprint.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({'message': 'Course not found'}), 404

    db.session.delete(course)
    db.session.commit()
    return jsonify({'message': 'Course deleted successfully'})

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
