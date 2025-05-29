from flask import Blueprint, jsonify, request
from src.models.pedido_model import Pedido
from datetime import datetime
from src.services.pedido_service import PedidoService
from flask_jwt_extended import jwt_required

pedido = Blueprint('pedido', __name__)

@pedido.route('/pedido', methods=['POST'])
def register_pedido():
    hora = datetime.now()

    try:
        total = request.json['total']
        productos = request.json['productos']
        extras = request.json['extras']
        fecha_hora = hora
        pedido = Pedido(total, fecha_hora)

        exito, mensaje, pedido_id = PedidoService().post_pedido(pedido, productos, extras)

        if exito:
            return jsonify({'mensaje' : mensaje, 'pedido_id': pedido_id})
        else:
            return jsonify({'mensaje' : 'No se pudo registrar pedido'})
    except Exception as ex:
        import traceback
        print("Error en register_pedido:", ex)
        traceback.print_exc()
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
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
