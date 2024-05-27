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
            return jsonify({'mensaje' : 'No se pudo registrar el admin', 'error': mensaje})
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
@admin.route('/admin/<int:id>', methods=['GET'])
def get_admin(id):
    try:
        admin = Admin_Service.get_admin_by_id(id)
        if admin:
            return jsonify(admin)
        else:
            return jsonify({'mensaje': 'No se encontro admin'} )
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@admin.route('/admin/<int:id>', methods=['PUT'])
def actualizar_admin(id):
    try:
        username = request.json['username']
        password = request.json['password']

        hash = bcrypt.generate_password_hash(password).decode('utf-8')
        admin = Admin(username, hash, id)
    
        exito, mensaje = Admin_Service.update_admin(admin)

        if exito:
            return jsonify({'mensaje' : mensaje})
        else:
            return jsonify({'mensaje' : f'No se encontro admin: {mensaje}'})
    except Exception as ex:
         return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
