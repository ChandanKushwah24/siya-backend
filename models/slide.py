from api_server import db
from datetime import datetime
import uuid

class Slide(db.Model):
    """Slide model representing a presentation slide in the system.
    
    This model stores information about individual slides including their content,
    theme, and ownership. Each slide belongs to a user and can have an associated theme.
    
    """
    __tablename__ = 'slides'
    __bind_key__ = 'db_key'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200))
    content = db.Column(db.JSON)
    theme_id = db.Column(db.String(36), db.ForeignKey('themes.id'))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    theme = db.relationship('Theme', backref='slides')
    user = db.relationship('User', backref='slides')