from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended.jwt_manager import JWTManager
from .routes import categoria, extra, producto, admin, auth, pedido, pedido_producto, pedido_extra
from flask_cors import CORS
from flask_wtf import CSRFProtect

def init_app(config):
    app = Flask(__name__)

    # Configuracion
    app.config.from_object(config)

    Bcrypt(app)
    JWTManager(app)

    csrf = CSRFProtect()
    csrf.init_app(app)

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
    app.register_blueprint(auth)
    app.register_blueprint(pedido)
    app.register_blueprint(pedido_producto)
    app.register_blueprint(pedido_extra)

    return app
