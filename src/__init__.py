from flask import Flask
from .routes import Producto_Routes, Categoria_Routes, Extra_Routes

app = Flask(__name__)

def init_app(config):
    # Configuracion
    app.config.from_object(config)
    
    # Blueprints
    app.register_blueprint(Producto_Routes.main, url_prefix='/producto')
    app.register_blueprint(Categoria_Routes.main, url_prefix='/categoria')
    app.register_blueprint(Extra_Routes.main, url_prefix='/extra')

    return app