from flask import Blueprint, jsonify, request
from src.models.pedido_model import Pedido
from datetime import datetime
from src.services.pedido_service import Pedido_Service

pedido = Blueprint('pedido', __name__)

@pedido.route('/pedido', methods=['POST'])
def register_pedido():
    hora = datetime.now()

    try:
        total = request.json['total']
        fecha_hora = hora
        pedido = Pedido(total, fecha_hora)

        exito, mensaje = Pedido_Service().post_pedido(pedido)

        if exito:
            return jsonify({'mensaje' : mensaje})
        else:
            return jsonify({'mensaje' : 'No se pudo registrar pedido'})
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
@pedido.route('/pedido', methods=['GET'])
def listar_pedido():
    try:
        pedidos = Pedido_Service.get_pedido()
        if pedidos:
            return jsonify(pedidos)
        else:
            return jsonify([])
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
