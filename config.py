import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:your_new_password@127.0.0.1:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
