from config import confi
from src import init_app
from flask_jwt_extended import JWTManager

from decouple import config

configuration = confi['development']
port = int(config('PORT', default=4000))
app = init_app(configuration)
jwt = JWTManager(app)

if __name__=='__main__':
    app.run(host='0.0.0.0', port = port)
