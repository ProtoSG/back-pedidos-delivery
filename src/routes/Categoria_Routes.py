from flask import Blueprint, request, jsonify
from src.models.categoria_model import Categoria
from src.services.categoria_service import CategoriaService
from flask_jwt_extended import jwt_required

categoria = Blueprint('categoria', __name__)

@categoria.route('/categoria', methods=['POST'])
@jwt_required()
def registrar_categoria():
    try:
        nombre = request.json['nombre']
        categoria = Categoria(nombre)
        exito, mensaje = CategoriaService.post_categoria(categoria)
        if exito:
            return jsonify({'mensaje' : mensaje})
        else:
            return jsonify({'mensaje' : 'No se pudo registrar el producto'})
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500


@categoria.route('/categoria', methods=['GET'])
def listar_categoria():
    """
    Endpoint para listar todas las categorías.
    Returns:
        JSON: Lista de categorías o mensaje de error.
    """
    try:
        categorias = CategoriaService.get_categoria()

        if categorias:
            return jsonify(categorias)
        else:
            return jsonify([])
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
        
@categoria.route('/categoria/<int:id>', methods=['GET'])
def obtener_categoria(id):
    """
    Endpoint para obtener una categoría por su ID.
    Args:
        id (int): ID de la categoría.
    Returns:
        JSON: Categoría encontrada o mensaje de error.
    """
    try:
        categoria = CategoriaService.get_categoria_by_id(id)
        if categoria:
            return jsonify(categoria)
        else:
            return jsonify({'mensaje': 'No se encontro categoria'} )
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
@categoria.route('/categoria/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_categoria(id):
    try:
        nombre = request.json['nombre']

        categoria = Categoria(nombre, id)
        
        exito, mensaje = CategoriaService.update_categoria(categoria)
        if exito:
            return jsonify({'mensaje' : mensaje})
        else:
            return jsonify({'mensaje' : ' No se encontro producto'})
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
@categoria.route('/categoria/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_categoria(id):
    try:
        exito, mensaje = CategoriaService.delete_categoria(id)
        if exito:
            return jsonify({'mensaje': mensaje})
        else:
            return jsonify({'mensaje' : 'No se encontro producto'})
    except Exception as ex:
         return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
@categoria.route('/categoria/rank/<string:date>', methods=['GET'])
def listar_rank_categoria(date):
    try:
        categorias = CategoriaService.get_rank(date)
        if categorias:
            return jsonify(categorias)
        return jsonify([])
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
