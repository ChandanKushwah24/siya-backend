from api_server import db
from datetime import datetime

class Theme(db.Model):
    __tablename__ = 'themes'
    __bind_key__ = 'db_key'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    background_color = db.Column(db.String(50))
    text_color = db.Column(db.String(50))
    font_family = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Template(db.Model):
    __tablename__ = 'templates'
    __bind_key__ = 'db_key'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    layout = db.Column(db.JSON, nullable=False)
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    theme = db.relationship('Theme', backref='templates')

class Slide(db.Model):
    __tablename__ = 'slides'
    __bind_key__ = 'db_key'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    content = db.Column(db.JSON)
    template_id = db.Column(db.Integer, db.ForeignKey('templates.id'))
    theme_id = db.Column(db.Integer, db.ForeignKey('themes.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    template = db.relationship('Template', backref='slides')
    theme = db.relationship('Theme', backref='slides')
    user = db.relationship('User', backref='slides')