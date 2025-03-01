import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:saro%402003@localhost:5432/booking'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
