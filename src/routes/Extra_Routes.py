from flask import Blueprint, request, jsonify
from src.models.extra_model import Extra
from src.services.extra_service import ExtraService
from flask_jwt_extended import jwt_required

extra = Blueprint('extra', __name__)

@extra.route('/extra', methods=['POST'])
@jwt_required()
def registrar_extra():
    try:
        nombre = request.json['nombre']
        precio = request.json['precio']
        imagen_url = request.json['imagen_url']
        extra = Extra(nombre, precio, imagen_url)
        exito, mensaje = ExtraService.post_extra(extra)
        if exito:
            return jsonify({'mensaje' : mensaje})
        else:
            return jsonify({'mensaje' : 'No se pudo registrar el producto'})
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@extra.route('/extra', methods=['GET'])
def listar_extra():
    """
    Endpoint para listar todos los extras.
    Returns:
        JSON: Lista de extras o mensaje de error.
    """
    try:
        extras = ExtraService.get_extra()

        if extras:
            return jsonify(extras)
        else:
            return jsonify([])
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
        
@extra.route('/extra/<int:id>', methods=['GET'])
def obtener_extra(id):
    """
    Endpoint para obtener un extra por su ID.
    Args:
        id (int): ID del extra.
    Returns:
        JSON: Extra encontrado o mensaje de error.
    """
    try:
        extra = ExtraService.get_extra_by_id(id)
        if extra:
            return jsonify(extra)
        else:
            return jsonify({'mensaje': 'No se encontro extra'} )
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
@extra.route('/extra/<int:id>', methods=['PUT'])
@jwt_required()
def actualizar_extra(id):
    try:
        nombre = request.json['nombre']
        precio = request.json['precio']
        imagen_url = request.json['imagen_url']
        extra = Extra(nombre, precio, imagen_url, id)
        
        exito, mensaje = ExtraService.update_extra(extra)
        if exito:
            return jsonify({'mensaje' : mensaje})
        else:
            return jsonify({'mensaje' : ' No se encontro producto'})
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
@extra.route('/extra/<int:id>', methods=['DELETE'])
@jwt_required()
def eliminar_extra(id):
    try:
        exito, mensaje = ExtraService.delete_extra(id)
        if exito:
            return jsonify({'mensaje': mensaje})
        else:
            return jsonify({'mensaje' : 'No se encontro producto'})
    except Exception as ex:
         return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
