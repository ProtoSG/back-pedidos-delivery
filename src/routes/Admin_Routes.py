from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from src.models.admin_model import Admin
from src.services.admin_service import AdminService

admin = Blueprint('admin', __name__)
bcrypt = Bcrypt()

@admin.route('/admin', methods=['POST'])
def registrar_admin():
    try:
        username = request.json['username']
        password = request.json['password']
        admin_exist = AdminService.get_admin_by_username(username)

        if admin_exist:
            return jsonify({'mensaje': 'El admin ya existe'}), 400

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        admin = Admin(username, password_hash)
        exito, mensaje = AdminService.post_admin(admin)
        if exito:
            # Generar token JWT para el nuevo admin
            acces_token = create_access_token(identity=username)
            return jsonify({'mensaje': mensaje, 'token': acces_token, 'username': username})
        else:
            return jsonify({'mensaje' : 'No se pudo registrar el admin', 'error': mensaje})
    except Exception as ex:
        import traceback
        print("Error en registrar_admin:", ex)
        traceback.print_exc()
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@admin.route('/admin/<int:id>', methods=['GET'])
def get_admin(id):
    try:
        admin = AdminService.get_admin_by_id(id)
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

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
        admin = Admin(username, password_hash, id)

        exito, mensaje = AdminService.update_admin(admin)

        if exito:
            return jsonify({'mensaje' : mensaje})
        else:
            return jsonify({'mensaje' : f'No se encontro admin: {mensaje}'})
    except Exception as ex:
         return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
