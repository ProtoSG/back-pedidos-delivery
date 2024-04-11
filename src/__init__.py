from flask import Flask
from .routes import categoria, extra, producto
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def init_app(config):
    # Configuracion
    app.config.from_object(config)
    
    # Blueprints
    app.register_blueprint(categoria)
    app.register_blueprint(extra)
    app.register_blueprint(producto)


    return app