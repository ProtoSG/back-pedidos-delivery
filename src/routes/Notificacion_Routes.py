from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.services.notificacion_service import NotificacionService
from src.services.usuario_service import UsuarioService
import traceback

notificacion = Blueprint('notificacion', __name__)

@notificacion.route('/notificaciones', methods=['GET'])
@jwt_required()
def get_notificaciones_usuario():
    try:
        email_actual = get_jwt_identity()

        usuario_data = UsuarioService.get_usuario_by_email(email_actual)

        if not usuario_data:
            print(f"ERROR: Usuario con email {email_actual} no encontrado")
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

        # Obtener parámetro opcional para filtrar solo no leídas
        solo_no_leidas = request.args.get('no_leidas', 'false').lower() == 'true'

        # Verificar que usuario_data contiene lo esperado
        if 'id' not in usuario_data:
            print(f"ERROR: El objeto usuario_data no contiene el campo 'id': {usuario_data.keys()}")
            return jsonify({'mensaje': 'Error en datos de usuario'}), 500

        notificaciones = NotificacionService.get_notificaciones_usuario(
            usuario_data['id'],
            solo_no_leidas=solo_no_leidas
        )

        # Debug adicional
        if not notificaciones or len(notificaciones) == 0:
            print(f"INFO: No se encontraron notificaciones para usuario_id: {usuario_data['id']}")

        return jsonify({
            'notificaciones': notificaciones,
            'total': len(notificaciones),
            'usuario_id': usuario_data['id']
        }), 200

    except Exception as ex:
        traceback.print_exc()
        print(f"ERROR en get_notificaciones_usuario: {str(ex)}")
        return jsonify({
            'mensaje': f'Error interno del servidor: {str(ex)}',
            'error': True,
            'tipo_error': str(type(ex).__name__)
        }), 500

@notificacion.route('/notificaciones/resumen', methods=['GET'])
@jwt_required()
def get_resumen_notificaciones():
    try:
        email_actual = get_jwt_identity()
        usuario_data = UsuarioService.get_usuario_by_email(email_actual)

        if not usuario_data:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

        resumen = NotificacionService.get_resumen_notificaciones(usuario_data['id'])

        return jsonify(resumen), 200

    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@notificacion.route('/notificaciones/<int:notificacion_id>/marcar-leida', methods=['PUT'])
@jwt_required()
def marcar_notificacion_leida(notificacion_id):
    try:
        email_actual = get_jwt_identity()
        usuario_data = UsuarioService.get_usuario_by_email(email_actual)

        if not usuario_data:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

        # Verificar que la notificación exista y pertenezca al usuario
        print(f"INFO: Verificando notificación {notificacion_id} para usuario {usuario_data['id']}")
        notificaciones = NotificacionService.get_notificaciones_usuario(usuario_data['id'])
        notificacion_encontrada = False

        for notif in notificaciones:
            if notif.get('id') == notificacion_id:
                notificacion_encontrada = True
                break

        if not notificacion_encontrada:
            print(f"ERROR: Notificación {notificacion_id} no encontrada o no pertenece al usuario {usuario_data['id']}")
            return jsonify({'mensaje': 'Notificación no encontrada o no pertenece al usuario'}), 404

        print(f"INFO: Marcando notificación {notificacion_id} como leída")
        exito, mensaje = NotificacionService.marcar_como_leida(notificacion_id)

        if exito:
            return jsonify({'mensaje': mensaje}), 200
        else:
            return jsonify({'mensaje': mensaje}), 400

    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@notificacion.route('/notificaciones/marcar-todas-leidas', methods=['PUT'])
@jwt_required()
def marcar_todas_notificaciones_leidas():
    try:
        email_actual = get_jwt_identity()
        usuario_data = UsuarioService.get_usuario_by_email(email_actual)

        if not usuario_data:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

        exito, mensaje = NotificacionService.marcar_todas_como_leidas(usuario_data['id'])

        if exito:
            return jsonify({'mensaje': mensaje}), 200
        else:
            return jsonify({'mensaje': mensaje}), 400

    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@notificacion.route('/notificaciones/<int:notificacion_id>', methods=['DELETE'])
@jwt_required()
def eliminar_notificacion(notificacion_id):
    try:
        email_actual = get_jwt_identity()
        usuario_data = UsuarioService.get_usuario_by_email(email_actual)

        if not usuario_data:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

        exito, mensaje = NotificacionService.eliminar_notificacion(notificacion_id, usuario_data['id'])

        if exito:
            return jsonify({'mensaje': mensaje}), 200
        else:
            return jsonify({'mensaje': mensaje}), 400

    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

# Ruta administrativa para crear notificaciones (solo para admins)
@notificacion.route('/admin/notificaciones', methods=['POST'])
@jwt_required()
def crear_notificacion_admin():
    try:
        # Esta ruta podría requerir validación de rol de admin
        # Por ahora permitimos crear notificaciones si se proporciona usuario_id

        if not request.json:
            return jsonify({'mensaje': 'La solicitud debe incluir datos JSON'}), 400

        campos_requeridos = ['usuario_id', 'mensaje']
        for campo in campos_requeridos:
            if campo not in request.json:
                return jsonify({'mensaje': f'El campo {campo} es obligatorio'}), 400

        usuario_id = request.json['usuario_id']
        pedido_id = request.json.get('pedido_id')
        mensaje = request.json['mensaje']
        tipo = request.json.get('tipo', 'info')

        # Log de datos recibidos
        print(f"INFO: Datos recibidos - usuario_id: {usuario_id}, pedido_id: {pedido_id}, tipo: {tipo}")

        # Verificar que el usuario existe
        usuario = UsuarioService.get_usuario_by_id(usuario_id)
        if not usuario:
            print(f"ERROR: Usuario {usuario_id} no encontrado en la base de datos")
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

        print(f"INFO: Creando notificación admin para usuario {usuario_id}, pedido {pedido_id}")
        exito, mensaje_resultado, notificacion_id = NotificacionService.crear_notificacion(
            usuario_id, pedido_id, mensaje, tipo
        )

        if exito:
            print(f"INFO: Notificación creada exitosamente con ID: {notificacion_id}")
            return jsonify({
                'mensaje': mensaje_resultado,
                'tipo': tipo,
                'creada': True,
                'notificacion_id': notificacion_id
            }), 201
        else:
            print(f"ERROR: No se pudo crear notificación: {mensaje_resultado}")
            return jsonify({
                'mensaje': mensaje_resultado,
                'error': True,
                'detalles': {
                    'usuario_id': usuario_id,
                    'pedido_id': pedido_id,
                    'tipo': tipo
                }
            }), 400

    except Exception as ex:
        traceback.print_exc()
        print(f"ERROR en crear_notificacion_admin: {str(ex)}")
        return jsonify({
            'mensaje': f'Error interno del servidor: {str(ex)}',
            'error': True,
            'tipo_error': str(type(ex).__name__)
        }), 500
