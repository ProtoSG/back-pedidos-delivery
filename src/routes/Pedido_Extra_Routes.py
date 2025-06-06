from flask import Blueprint, jsonify
from src.services.pedido_extra_service import PedidoExtraService
from flask_jwt_extended import jwt_required

pedido_extra = Blueprint('pedido_extra', __name__)
    
@pedido_extra.route('/pedido_extra/<int:id>', methods=['GET'])
@jwt_required()
def get_pedido_extra(id):
    try:
        pedidos_extras = PedidoExtraService.get_pedido_extra(id)
        if pedidos_extras:
            return jsonify(pedidos_extras)
        return jsonify([])
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500



@pedido_extra.route('/pedido_extra/rank_extra/<string:date>', methods=['GET'])
def listar_rank_extras(date):
    try:
        extras = PedidoExtraService.get_rank_extra(date)
        if extras:
            return jsonify(extras)
        return jsonify([])
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
