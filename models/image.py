from api_server import db
from datetime import datetime
import uuid


class Image(db.Model):
    __tablename__ = 'images'
    __bind_key__ = 'db_key'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    filename = db.Column(db.String(255), nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)
    mimetype = db.Column(db.String(100), nullable=False)
    size = db.Column(db.Integer)
    slide_id = db.Column(db.String(36), db.ForeignKey('slides.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
