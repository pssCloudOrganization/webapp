# app/config.py
import os
import logging
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    
    # Logging configuration
    LOG_LEVEL = logging.INFO
    LOG_FILE_PATH = '/var/log/webapp/csye6225.log'
    
    # StatsD configuration
    STATSD_HOST = 'localhost'
    STATSD_PORT = 8125
    STATSD_PREFIX = 'webapp'

class TestConfig(Config):
    LOG_LEVEL = logging.INFO
    LOG_FILE_PATH = 'csye6225.log'
    
    # StatsD configuration
    STATSD_HOST = 'localhost'
    STATSD_PORT = 8125
    STATSD_PREFIX = 'webapp'
    TESTING = True
    PROPAGATE_EXCEPTIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL')
    LOG_LEVEL = logging.DEBUG
