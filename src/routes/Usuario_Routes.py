from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.services.usuario_service import UsuarioService
from src.models.usuario_model import Usuario
import re

usuario = Blueprint('usuario', __name__)

@usuario.route('/usuario/registro', methods=['POST'])
def registrar_usuario():
    try:
        if not request.json:
            return jsonify({'mensaje': 'La solicitud debe incluir datos JSON'}), 400

        # Validar campos requeridos
        campos_requeridos = ['nombre', 'email', 'password']
        for campo in campos_requeridos:
            if campo not in request.json or not request.json[campo]:
                return jsonify({'mensaje': f'El campo {campo} es obligatorio'}), 400

        nombre = request.json['nombre'].strip()
        email = request.json['email'].strip().lower()
        password = request.json['password']

        # Validaciones adicionales
        if len(nombre) < 2:
            return jsonify({'mensaje': 'El nombre debe tener al menos 2 caracteres'}), 400

        # Validar formato de email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return jsonify({'mensaje': 'El formato del email no es válido'}), 400

        # Validar contraseña
        if len(password) < 6:
            return jsonify({'mensaje': 'La contraseña debe tener al menos 6 caracteres'}), 400

        # Crear objeto usuario
        nuevo_usuario = Usuario(nombre=nombre, email=email, password=password)

        # Registrar usuario
        exito, mensaje = UsuarioService.registrar_usuario(nuevo_usuario)

        if exito:
            return jsonify({'mensaje': mensaje}), 201
        else:
            return jsonify({'mensaje': mensaje}), 400

    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@usuario.route('/usuario/login', methods=['POST'])
def login_usuario():
    try:
        if not request.json or 'email' not in request.json or 'password' not in request.json:
            return jsonify({'mensaje': 'La solicitud JSON debe incluir "email" y "password"'}), 400

        email = request.json['email'].strip().lower()
        password = request.json['password']

        print(f"INFO: Intento de login para usuario: {email}")

        # Validar login
        exito, resultado = UsuarioService.login_usuario(email, password)

        if exito:
            # Crear token de acceso
            access_token = create_access_token(identity=email)
            print(f"INFO: Login exitoso para usuario: {email}")

            return jsonify({
                'mensaje': 'Login exitoso',
                'usuario': resultado,
                'token': access_token
            }), 200
        else:
            print(f"ERROR: Login fallido para usuario: {email} - {resultado}")
            return jsonify({'mensaje': resultado}), 401

    except Exception as ex:
        print(f"ERROR: Excepción en login_usuario: {str(ex)}")
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@usuario.route('/usuario/perfil', methods=['GET'])
@jwt_required()
def get_perfil_usuario():
    try:
        email_actual = get_jwt_identity()
        usuario_data = UsuarioService.get_usuario_by_email(email_actual)

        if usuario_data:
            # No incluir la contraseña en la respuesta
            del usuario_data['password']
            return jsonify(usuario_data), 200
        else:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@usuario.route('/usuario/perfil', methods=['PUT'])
@jwt_required()
def actualizar_perfil_usuario():
    try:
        if not request.json:
            return jsonify({'mensaje': 'La solicitud debe incluir datos JSON'}), 400

        email_actual = get_jwt_identity()
        usuario_actual = UsuarioService.get_usuario_by_email(email_actual)

        if not usuario_actual:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

        # Obtener datos a actualizar
        nombre = request.json.get('nombre', usuario_actual['nombre']).strip()
        email_nuevo = request.json.get('email', usuario_actual['email']).strip().lower()

        # Validaciones
        if len(nombre) < 2:
            return jsonify({'mensaje': 'El nombre debe tener al menos 2 caracteres'}), 400

        # Validar formato de email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email_nuevo):
            return jsonify({'mensaje': 'El formato del email no es válido'}), 400

        # Si el email cambió, verificar que no esté en uso por otro usuario
        if email_nuevo != usuario_actual['email']:
            usuario_existente = UsuarioService.get_usuario_by_email(email_nuevo)
            if usuario_existente and usuario_existente['id'] != usuario_actual['id']:
                return jsonify({'mensaje': 'El email ya está en uso por otro usuario'}), 400

        # Crear objeto usuario actualizado
        usuario_actualizado = Usuario(
            nombre=nombre,
            email=email_nuevo,
            password=usuario_actual['password'],  # Mantener la contraseña actual
            usuario_id=usuario_actual['id']
        )

        # Actualizar usuario
        exito, mensaje = UsuarioService.actualizar_usuario(usuario_actualizado)

        if exito:
            return jsonify({'mensaje': mensaje}), 200
        else:
            return jsonify({'mensaje': mensaje}), 400

    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@usuario.route('/usuario/cambiar-password', methods=['PUT'])
@jwt_required()
def cambiar_password():
    try:
        if not request.json or 'password_actual' not in request.json or 'password_nueva' not in request.json:
            return jsonify({'mensaje': 'Se requieren "password_actual" y "password_nueva"'}), 400

        email_actual = get_jwt_identity()
        usuario_data = UsuarioService.get_usuario_by_email(email_actual)

        if not usuario_data:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

        password_actual = request.json['password_actual']
        password_nueva = request.json['password_nueva']

        # Validar contraseña actual
        exito_login, _ = UsuarioService.login_usuario(email_actual, password_actual)
        if not exito_login:
            return jsonify({'mensaje': 'La contraseña actual es incorrecta'}), 401

        # Validar nueva contraseña
        if len(password_nueva) < 6:
            return jsonify({'mensaje': 'La nueva contraseña debe tener al menos 6 caracteres'}), 400

        # Cambiar contraseña
        exito, mensaje = UsuarioService.cambiar_password(usuario_data['id'], password_nueva)

        if exito:
            return jsonify({'mensaje': mensaje}), 200
        else:
            return jsonify({'mensaje': mensaje}), 400

    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@usuario.route('/usuario/desactivar', methods=['PUT'])
@jwt_required()
def desactivar_cuenta():
    try:
        email_actual = get_jwt_identity()
        usuario_data = UsuarioService.get_usuario_by_email(email_actual)

        if not usuario_data:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

        # Desactivar usuario
        exito, mensaje = UsuarioService.desactivar_usuario(usuario_data['id'])

        if exito:
            return jsonify({'mensaje': mensaje}), 200
        else:
            return jsonify({'mensaje': mensaje}), 400

    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@usuario.route('/usuario/validar-token', methods=['GET'])
@jwt_required()
def validar_token():
    try:
        email_actual = get_jwt_identity()
        usuario_data = UsuarioService.get_usuario_by_email(email_actual)

        if not usuario_data:
            return jsonify({'valido': False, 'mensaje': f'Usuario con email {email_actual} no encontrado'}), 401

        if not usuario_data.get('activo'):
            return jsonify({'valido': False, 'mensaje': 'Usuario inactivo'}), 401

        # No incluir la contraseña en la respuesta
        del usuario_data['password']
        return jsonify({
            'valido': True,
            'usuario': usuario_data
        }), 200

    except Exception as ex:
        return jsonify({'valido': False, 'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
