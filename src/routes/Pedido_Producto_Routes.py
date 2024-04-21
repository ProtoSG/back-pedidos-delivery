from flask import Blueprint, jsonify, request
from src.models.pedido_producto_model import Pedido_Producto
from src.services.pedido_producto_service import Pedido_Producto_Service
from flask_jwt_extended import jwt_required

pedido_producto = Blueprint('pedido_producto', __name__)
    
@pedido_producto.route('/pedido_producto/<int:id>', methods=['GET'])
@jwt_required()
def get_pedido_producto(id):
    try:
        pedidos_productos = Pedido_Producto_Service.get_pedido_producto(id)
        if pedidos_productos:
            return jsonify(pedidos_productos)
        
        return jsonify([])
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500


@pedido_producto.route('/pedido_producto/rank_productos/<string:date>', methods=['GET'])
def listar_rank_productos(date):
    try:
        pedidos = Pedido_Producto_Service.get_rank_producto(date)
        if pedidos:
            return jsonify(pedidos)
        return jsonify([])
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500