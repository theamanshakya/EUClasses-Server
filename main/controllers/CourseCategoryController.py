import datetime
import os
from flask import Blueprint, request, jsonify
from flask_uploads import UploadSet, IMAGES, configure_uploads
from fileinput import filename 
from werkzeug.utils import secure_filename

import json
from main import app
from main.models.CourseCategory import CourseCategory
from flask import request
from main import db
course_categories_blueprint = Blueprint('course_categories', __name__)

photos = UploadSet('photos', IMAGES)
app.config['UPLOAD_FOLDER'] = "main/static/img"
app.config['UPLOADED_PHOTOS_DEST'] = 'main/static/img'
configure_uploads(app, photos)




ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@course_categories_blueprint.route('/course-categories', methods=['GET'])
def get_course_categories():
    categories = CourseCategory.query.all()
    return jsonify({'categories': [category.to_dict() for category in categories]})

@course_categories_blueprint.route('/course-categories/<int:category_id>', methods=['GET'])
def get_course_category(category_id):
    category = CourseCategory.query.get(category_id)
    if category:
        return jsonify({'category': category.to_dict()})
    else:
        return jsonify({'message': 'Course category not found'}), 404

@course_categories_blueprint.route('/course-categories', methods=['POST'])
def create_category():
    
    title = request.form['title']
    description = request.form['description']

    image = request.files['file']
    print("Image type is ",type(image))
    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)  # Sanitize filename
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
        image_url = f"/static/img/{filename}"
    else:
        return jsonify({'error':'Invalid file or no file part'}), 400

    try:
        new_category = CourseCategory(title=title, description=description, image_url=image_url)
        db.session.add(new_category)
        db.session.commit()

        return jsonify({'message': 'Course category created successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create category: ' + str(e)}), 500


@course_categories_blueprint.route('/course-categories/<int:category_id>', methods=['PUT'])
def update_course_category(category_id):
    category = CourseCategory.query.get(category_id)
    if not category:
        return jsonify({'message': 'Course category not found'}), 404

    data = request.get_json() or {}  
    category.title = data.get('title', category.title)
    category.description = data.get('description', category.description)

    if 'photo' in request.files:
        photo = request.files['photo']
        if photo and allowed_file(photo.filename):
            if category.image:
                photos.delete(category.image)  
            image_filename = photos.save(photo)
            category.image = image_filename

    db.session.commit()
    return jsonify({'message': 'Course category updated successfully'})

@course_categories_blueprint.route('/course-categories/<int:category_id>', methods=['DELETE'])
def delete_course_category(category_id):
    category = CourseCategory.query.get(category_id)
    if not category:
        return jsonify({'message': 'Course category not found'}), 404

    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Course category deleted successfully'})

