from decouple import config

class Config():
    def __init__(self):
        self.SECRET_KEY = config('SECRET_KEY')
        self.JWT_SECRET_KEY = config('JWT_SECRET_KEY')

class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self.DEBUG = True

confi = {
    'development': DevelopmentConfig()
}