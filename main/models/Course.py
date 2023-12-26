from main import db
from datetime import datetime

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    language = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    thumbnail = db.Column(db.String(255), nullable=True)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'language': self.language,
            'duration': self.duration,
            'description': self.description,
            'thumbnail': self.thumbnail,
            'price': self.price,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
