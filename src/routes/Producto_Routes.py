from flask import Blueprint, request, jsonify
from src.models.producto_model import Producto
from src.services.producto_service import Producto_Service

main = Blueprint('producto', __name__)

@main.route('/', methods=['POST'])
def registrar_producto():
    try:
        nombre = request.json['nombre']
        categoria_id = request.json['categoria_id']
        precio = request.json['precio']

        _producto = Producto(nombre, categoria_id, precio)

        exito, mensaje = Producto_Service.post_producto(_producto)

        if exito:
            return jsonify({'mensaje' : mensaje})
        else:
            return jsonify({'mensaje': 'No se pudo registrar el producto'})
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
@main.route('/', methods=['GET'])
def listar_producto():
    try:
        productos = Producto_Service.get_producto()

        if productos:
            return jsonify(productos)
        else:
            return jsonify({'mensaje': 'No hay productos'})
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
        
@main.route('/<int:id>', methods=['GET'])
def obtener_producto(id):
    try:
        producto = Producto_Service.get_producto_by_id(id)
        if producto:
            return jsonify(producto)
        else:
            return jsonify({'mensaje': 'No se encontro producto'} )
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
@main.route('/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    try:
        nombre = request.json['nombre']
        categoria = request.json['categoria']
        precio = request.json['precio']

        producto = Producto(nombre, categoria, precio, id)
        
        exito, mensaje = Producto_Service.update_prodcuto(producto)
        if exito:
            return jsonify({'mensaje' : mensaje})
        else:
            return jsonify({'mensaje' : ' No se encontro producto'})
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
@main.route('/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        exito, mensaje = Producto_Service.delete_producto(id)
        if exito:
            return jsonify({'mensaje': mensaje})
        else:
            return jsonify({'mensaje' : 'No se encontro producto'})
    except Exception as ex:
         return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    