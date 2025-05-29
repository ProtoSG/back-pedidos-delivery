from flask import Blueprint, request, jsonify
from src.models.producto_model import Producto
from src.services.producto_service import ProductoService
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.database.db_mysql import get_connection

producto = Blueprint('producto', __name__)

@producto.route('/producto', methods=['POST'])
@jwt_required()
def registrar_producto():
    try:
        nombre = request.json['nombre']
        categoria_id = request.json['categoria_id']
        precio = request.json['precio']
        descripcion = request.json['descripcion']
        imagen_url = request.json['imagen_url']

        _producto = Producto(nombre, categoria_id, precio, descripcion, imagen_url)

        exito, mensaje = ProductoService.post_producto(_producto)

        if exito:
            return jsonify({'mensaje' : mensaje})
        else:
            return jsonify({'mensaje': f'No se pudo registrar el producto {mensaje}'})
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
@producto.route('/producto', methods=['GET'])
def listar_producto():
    try:
        productos = ProductoService.get_producto()
        if productos:
            return jsonify(productos)
        else:
            return jsonify([])
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
        
@producto.route('/producto/<int:id>', methods=['GET'])
def obtener_producto(id):
    try:
        producto = ProductoService.get_producto_by_id(id)
        if producto:
            return jsonify(producto)
        else:
            return jsonify({'mensaje': 'No se encontro producto'} )
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
@producto.route('/producto/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_producto(id):
    try:
        nombre = request.json['nombre']
        categoria_id = request.json['categoria_id']
        precio = request.json['precio']
        descripcion = request.json['descripcion']
        imagen_url = request.json['imagen_url']

        producto = Producto(nombre, categoria_id, precio, descripcion, imagen_url , id)
        
        exito, mensaje = ProductoService.update_prodcuto(producto)
        if exito:
            return jsonify({'mensaje' : mensaje})
        else:
            return jsonify({'mensaje' : ' No se encontro producto'})
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
@producto.route('/producto/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_producto(id):
    try:
        exito, mensaje = ProductoService.delete_producto(id)
        if exito:
            return jsonify({'mensaje': mensaje})
        else:
            return jsonify({'mensaje' : 'No se encontro producto'})
    except Exception as ex:
         return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
