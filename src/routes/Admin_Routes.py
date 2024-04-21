from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from src.models.admin_model import Admin
from src.services.admin_service import Admin_Service

admin = Blueprint('admin', __name__)
bcrypt = Bcrypt()

@admin.route('/admin', methods=['POST'])
def registrar_admin():
    try:
        username = request.json['username']
        password = request.json['password']

        admin_exist = Admin_Service.get_admin_by_username(username)

        if admin_exist:
            return jsonify({'mensaje': 'El admin ya existe'}), 400

        hash = bcrypt.generate_password_hash(password).decode('utf-8')
        admin = Admin(username, hash)
        exito, mensaje = Admin_Service.post_admin(admin)
        if exito:
            return jsonify({'mensaje' : mensaje})
        else:
            return jsonify({'mensaje' : 'No se pudo registrar el admin'})
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    

