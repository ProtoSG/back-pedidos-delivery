from flask import Blueprint, request, jsonify
from src.models.categoria_model import Categoria
from src.services.categoria_service import Categoria_Service

main = Blueprint('categoria', __name__)

@main.route('/', methods=['POST'])
def registrar_categoria():
    try:
        nombre = request.json['nombre']
        categoria = Categoria(nombre)
        exito, mensaje = Categoria_Service.post_categoria(categoria)
        if exito:
            return jsonify({'mensaje' : mensaje})
        else:
            return jsonify({'mensaje' : 'No se pudo registrar el producto'})
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@main.route('/', methods=['GET'])
def listar_categoria():
    try:
        categorias = Categoria_Service.get_categoria()

        if categorias:
            return jsonify(categorias)
        else:
            return jsonify({'mensaje': 'No hay productos'})
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
        
@main.route('/<int:id>', methods=['GET'])
def obtener_categoria(id):
    try:
        categoria = Categoria_Service.get_categoria_by_id(id)
        if categoria:
            return jsonify(categoria)
        else:
            return jsonify({'mensaje': 'No se encontro producto'} )
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
@main.route('/<int:id>', methods=['PUT'])
def actualizar_categoria(id):
    try:
        nombre = request.json['nombre']

        categoria = Categoria(nombre, id)
        
        exito, mensaje = Categoria_Service.update_categoria(categoria)
        if exito:
            return jsonify({'mensaje' : mensaje})
        else:
            return jsonify({'mensaje' : ' No se encontro producto'})
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
@main.route('/<int:id>', methods=['DELETE'])
def eliminar_categoria(id):
    try:
        exito, mensaje = Categoria_Service.delete_categoria(id)
        if exito:
            return jsonify({'mensaje': mensaje})
        else:
            return jsonify({'mensaje' : 'No se encontro producto'})
    except Exception as ex:
         return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    