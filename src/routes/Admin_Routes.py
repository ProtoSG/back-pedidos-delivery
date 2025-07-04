from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.admin_model import Admin
from src.services.admin_service import AdminService

admin = Blueprint('admin', __name__)
bcrypt = Bcrypt()

@admin.route('/admin', methods=['POST'])
def registrar_admin():
    """
    Endpoint para registrar un nuevo administrador.
    Returns:
        JSON: Mensaje de éxito o error.
    """
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

@admin.route('/admin', methods=['GET'])
def listar_admins():
    """
    Endpoint para listar todos los administradores.
    Returns:
        JSON: Lista de administradores o mensaje de error.
    """
    try:
        admins = AdminService.get_admins()
        if admins:
            return jsonify(admins)
        else:
            return jsonify([])
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@admin.route('/admin/<int:id>', methods=['GET'])
def obtener_admin(id):
    """
    Endpoint para obtener un administrador por su ID.
    Args:
        id (int): ID del administrador.
    Returns:
        JSON: Administrador encontrado o mensaje de error.
    """
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

@admin.route('/admin/validar-token', methods=['GET'])
@jwt_required()
def validar_token_admin():
    try:
        username_actual = get_jwt_identity()
        admin_data = AdminService.get_admin_by_username(username_actual)

        if not admin_data:
            print(f"ERROR: Admin con username {username_actual} no encontrado en la base de datos")
            return jsonify({'valido': False, 'mensaje': f'Admin con username {username_actual} no encontrado'}), 401

        # Si admin_data es un objeto, conviértelo a dict si es necesario
        if hasattr(admin_data, '__dict__'):
            admin_data = admin_data.__dict__
        if 'password' in admin_data:
            del admin_data['password']
        print(f"INFO: Token válido para admin {username_actual}")
        return jsonify({
            'valido': True,
            'admin': admin_data
        }), 200

    except Exception as ex:
        print(f"ERROR: Excepción en validar_token_admin: {str(ex)}")
        return jsonify({'valido': False, 'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
