import os
from datetime import timedelta

class Config:
    # Flask settings
    SECRET_KEY = 'your-secret-key-here'
    DEBUG = False

    # Database settings
    SQLALCHEMY_BINDS  = {'db_key': 'postgresql://postgres:root@localhost:5432/pitch_deck'}
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT settings
    JWT_SECRET_KEY = 'your-jwt-secret-key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
