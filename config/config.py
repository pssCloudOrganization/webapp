import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False

class TestConfig(Config):
    TESTING = True
    PROPAGATE_EXCEPTIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'