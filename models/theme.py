from api_server import db
from datetime import datetime
import uuid

class Theme(db.Model):
    """Theme model representing presentation styling configurations.
    """
    __tablename__ = 'themes'
    __bind_key__ = 'db_key'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    background_color = db.Column(db.String(50))
    text_color = db.Column(db.String(50))
    font_family = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
