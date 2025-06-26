from flask import Blueprint, jsonify, request
from src.models.pedido_model import Pedido
from datetime import datetime
from src.services.pedido_service import PedidoService
from src.services.usuario_service import UsuarioService
from flask_jwt_extended import jwt_required, get_jwt_identity
import traceback
import json

pedido = Blueprint('pedido', __name__)

@pedido.route('/pedido', methods=['POST'])
@jwt_required()
def register_pedido():
    hora = datetime.now()

    try:
        # Obtener usuario autenticado
        email_actual = get_jwt_identity()
        print("Email: ", email_actual)
        usuario_data = UsuarioService.get_usuario_by_email(email_actual)
        print("Email: ", usuario_data)

        if not usuario_data:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

        # Extraer datos de la solicitud
        try:
            request_data = request.get_json()
            if not request_data:
                return jsonify({'mensaje': 'Datos JSON no proporcionados'}), 400

            total = request_data.get('total')
            productos = request_data.get('productos', [])
            extras = request_data.get('extras', [])
        except Exception as e:
            return jsonify({'mensaje': f'Error en formato JSON: {str(e)}'}), 400

        # Validaciones básicas
        if total is None:
            return jsonify({'mensaje': 'El campo "total" es requerido'}), 400

        if not productos:
            return jsonify({'mensaje': 'Se requiere al menos un producto'}), 400

        # Validar estructura de productos
        for i, producto in enumerate(productos):
            if not isinstance(producto, dict):
                return jsonify({'mensaje': f'Producto #{i+1} con formato inválido'}), 400
            if 'producto_id' not in producto:
                return jsonify({'mensaje': f'Producto #{i+1} sin producto_id'}), 400
            if 'cantidad' not in producto:
                return jsonify({'mensaje': f'Producto #{i+1} sin cantidad'}), 400
            if 'sub_total' not in producto:
                return jsonify({'mensaje': f'Producto #{i+1} sin sub_total'}), 400

        # Logs para depuración
        print(f"INFO: Creando pedido para usuario {usuario_data['id']}")
        print(f"INFO: Total: {total}, tipo: {type(total)}")
        print(f"INFO: Productos: {len(productos)}")
        print(f"INFO: Extras: {len(extras) if extras else 0}")

        # Crear objeto pedido
        pedido_obj = Pedido(
            total=float(total) if total else 0.0,
            fecha_hora=hora,
            usuario_id=usuario_data['id'],
            estado='Pendiente'
        )

        # Intentar crear el pedido con transacción
        exito, mensaje, pedido_id = PedidoService().post_pedido(pedido_obj, productos, extras)
        print(f"INFO: Resultado creación - éxito: {exito}, mensaje: {mensaje}, ID: {pedido_id}")

        if exito:
            return jsonify({
                'mensaje': mensaje,
                'pedido_id': pedido_id,
                'estado': 'Pendiente',
                'fecha': hora.isoformat()
            }), 201  # 201 Created
        else:
            return jsonify({
                'mensaje': mensaje,
                'error': True,
                'detalles': {
                    'usuario_id': usuario_data['id'],
                    'total': total,
                    'num_productos': len(productos),
                    'num_extras': len(extras) if extras else 0
                }
            }), 400

    except Exception as ex:
        print("ERROR en register_pedido:")
        traceback.print_exc()
        return jsonify({
            'mensaje': f'Error interno del servidor',
            'detalle': str(ex)
        }), 500

@pedido.route('/pedido', methods=['GET'])
@jwt_required()
def listar_pedido():
    try:
        pedidos = PedidoService.get_pedido()
        if pedidos:
            return jsonify(pedidos)
        else:
            return jsonify([])
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@pedido.route('/pedido/datos_dias', methods=['GET'])
def listar_datos_dias():
    try:
        datos_dias = PedidoService.get_total_dia()
        if datos_dias:
            return jsonify(datos_dias)
        else:
            return jsonify([])
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@pedido.route('/pedido/datos_semanas', methods=['GET'])
def listar_datos_semanas():
    try:
        datos_semanas = PedidoService.get_total_semana()
        if datos_semanas:
            return jsonify(datos_semanas)
        else:
            return jsonify([])
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@pedido.route('/pedido/datos_meses', methods=['GET'])
def listar_datos_meses():
    try:
        datos_meses = PedidoService.get_total_mes()
        if datos_meses:
            return jsonify(datos_meses)
        else:
            return jsonify([])
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@pedido.route('/pedido/datos_anos', methods=['GET'])
def listar_datos_anos():
    try:
        datos_anos = PedidoService.get_total_ano()
        if datos_anos:
            return jsonify(datos_anos)
        else:
            return jsonify([])
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@pedido.route('/pedido/historial', methods=['GET'])
@jwt_required()
def get_historial_usuario():
    try:
        email_actual = get_jwt_identity()
        usuario_data = UsuarioService.get_usuario_by_email(email_actual)

        if not usuario_data:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

        historial = PedidoService.get_historial_usuario(usuario_data['id'])

        if historial:
            return jsonify({
                'historial': historial,
                'total_pedidos': len(historial)
            }), 200
        else:
            return jsonify({
                'historial': [],
                'total_pedidos': 0
            }), 200

    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@pedido.route('/pedido/mis-pedidos', methods=['GET'])
@jwt_required()
def get_mis_pedidos():
    try:
        email_actual = get_jwt_identity()
        usuario_data = UsuarioService.get_usuario_by_email(email_actual)

        if not usuario_data:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

        pedidos = PedidoService.get_pedidos_usuario(usuario_data['id'])

        return jsonify({
            'pedidos': pedidos,
            'total': len(pedidos)
        }), 200

    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@pedido.route('/pedido/<int:pedido_id>/estado', methods=['PUT'])
@jwt_required()
def actualizar_estado_pedido(pedido_id):
    try:
        # Verificar que el pedido existe
        pedido_data = PedidoService.get_pedido_by_id(pedido_id)
        if not pedido_data:
            return jsonify({'mensaje': f'Pedido #{pedido_id} no encontrado'}), 404

        # Verificar datos de entrada
        if not request.json or 'estado' not in request.json:
            return jsonify({'mensaje': 'Se requiere el campo "estado"'}), 400

        nuevo_estado = request.json['estado']

        # Validar estados permitidos
        estados_validos = ['Pendiente', 'Preparando', 'Enviado', 'Entregado', 'Cancelado']
        if nuevo_estado not in estados_validos:
            return jsonify({'mensaje': f'Estado inválido. Estados permitidos: {", ".join(estados_validos)}'}), 400

        print(f"INFO: Actualizando estado del pedido #{pedido_id} a '{nuevo_estado}'")

        # Actualizar estado usando transacción
        exito, mensaje = PedidoService.actualizar_estado_pedido(pedido_id, nuevo_estado)

        if exito:
            # Si el estado es "Enviado", también devolvemos información de notificación
            if nuevo_estado == 'Enviado':
                return jsonify({
                    'mensaje': mensaje,
                    'notificacion_creada': True,
                    'estado': nuevo_estado
                }), 200
            else:
                return jsonify({
                    'mensaje': mensaje,
                    'estado': nuevo_estado
                }), 200
        else:
            return jsonify({'mensaje': mensaje, 'error': True}), 400

    except Exception as ex:
        traceback.print_exc()
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@pedido.route('/pedido/<int:pedido_id>', methods=['GET'])
@jwt_required()
def get_pedido_detalle(pedido_id):
    try:
        email_actual = get_jwt_identity()
        usuario_data = UsuarioService.get_usuario_by_email(email_actual)

        if not usuario_data:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404

        pedido_data = PedidoService.get_pedido_by_id(pedido_id)

        if not pedido_data:
            return jsonify({'mensaje': 'Pedido no encontrado'}), 404

        # Verificar que el pedido pertenezca al usuario (o que sea admin)
        if pedido_data.get('usuario_id') != usuario_data['id']:
            return jsonify({'mensaje': 'No tienes permisos para ver este pedido'}), 403

        return jsonify(pedido_data), 200

    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
