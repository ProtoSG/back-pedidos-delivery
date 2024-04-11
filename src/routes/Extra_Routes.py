from flask import Blueprint, request, jsonify
from src.models.extra_model import Extra
from src.services.extra_service import Extra_Service

extra = Blueprint('extra', __name__)

@extra.route('/extra', methods=['POST'])
def registrar_extra():
    try:
        nombre = request.json['nombre']
        precio = request.json['precio']
        imagen_url = request.json['imagen_url']
        extra = Extra(nombre, precio, imagen_url)
        exito, mensaje = Extra_Service.post_extra(extra)
        if exito:
            return jsonify({'mensaje' : mensaje})
        else:
            return jsonify({'mensaje' : 'No se pudo registrar el producto'})
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

@extra.route('/extra', methods=['GET'])
def listar_extra():
    try:
        extras = Extra_Service.get_extra()

        if extras:
            return jsonify(extras)
        else:
            return jsonify([])
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
        
@extra.route('/extra/<int:id>', methods=['GET'])
def obtener_extra(id):
    try:
        extra = Extra_Service.get_extra_by_id(id)
        if extra:
            return jsonify(extra)
        else:
            return jsonify({'mensaje': 'No se encontro producto'} )
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
@extra.route('/extra/<int:id>', methods=['PUT'])
def actualizar_extra(id):
    try:
        nombre = request.json['nombre']
        precio = request.json['precio']
        imagen_url = request.json['imagen_url']
        extra = Extra(nombre, precio, imagen_url, id)
        
        exito, mensaje = Extra_Service.update_extra(extra)
        if exito:
            return jsonify({'mensaje' : mensaje})
        else:
            return jsonify({'mensaje' : ' No se encontro producto'})
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    
@extra.route('/extra/<int:id>', methods=['DELETE'])
def eliminar_extra(id):
    try:
        exito, mensaje = Extra_Service.delete_extra(id)
        if exito:
            return jsonify({'mensaje': mensaje})
        else:
            return jsonify({'mensaje' : 'No se encontro producto'})
    except Exception as ex:
         return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500
    