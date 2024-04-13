from config import config
from src import init_app
from flask_jwt_extended import JWTManager


configuration = config['development']
app = init_app(configuration)
jwt = JWTManager(app)

if __name__=='__main__':
    app.run()