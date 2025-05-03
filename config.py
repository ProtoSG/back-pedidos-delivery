import os
from dotenv import load_dotenv

class Config():
    load_dotenv()
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    ORIGIN_URL = os.environ.get("ORIGIN_URL")

class DevelopmentConfig(Config):
    DEBUG = False

confi = {
    'development': DevelopmentConfig
}
