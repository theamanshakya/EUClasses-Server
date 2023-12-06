from flask import jsonify
from app import app

@app.route('/', methods=['GET'])
def hello_world():
    return jsonify(message='Hello, World!')
