from decouple import config

class Config():
    SECRET_KEY = config('SECRET_KEY')
    JWT_SECRET_KEY = config('JWT_SECRET_KEY')

class DevelopmentConfig(Config):
    DEBUG = False

confi = {
    'development': DevelopmentConfig
}
