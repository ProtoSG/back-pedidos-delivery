from flask import Flask
from .routes import categoria, extra, producto, admin, login, pedido, pedido_producto, pedido_extra
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
    app.register_blueprint(admin)
    app.register_blueprint(login)
    app.register_blueprint(pedido)
    app.register_blueprint(pedido_producto)
    app.register_blueprint(pedido_extra)

    return app