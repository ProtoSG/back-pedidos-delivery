from flask import Flask
from .routes import categoria, extra, producto, admin, login, pedido, pedido_producto, pedido_extra
from flask_cors import CORS

def init_app(config):
    app = Flask(__name__)


    # Configuracion
    app.config.from_object(config)
    
    CORS(
        app, 
        origins=[app.config["ORIGIN_URL"]],
        supports_credentials=True
    )

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
