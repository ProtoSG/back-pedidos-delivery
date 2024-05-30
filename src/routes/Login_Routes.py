from flask import Blueprint, request, jsonify
from src.services.admin_service import Admin_Service
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt

login = Blueprint('login', __name__)
bcrypt = Bcrypt()

@login.route('/login', methods=['POST'])
def login_admin():
    try:
        if not request.json or 'username' not in request.json or 'password' not in request.json:
            return jsonify({'mensaje': 'La solicitud JSON debe incluir "username" y "password"'}), 400

        username = request.json['username']
        password = request.json['password']

        admin = Admin_Service.get_admin_by_username(username)

        print(admin)

        if not admin:
            return jsonify({'mensaje': 'El admin no existe'}), 404

        pw_hash = admin.get('password')
        
        if not bcrypt.check_password_hash(pw_hash, password):
            return jsonify({'mensaje': 'Contraseña incorrecta'}), 401

        acces_token = create_access_token(identity=username)

        response = jsonify({'id' : admin.get('id'), 'username':admin.get('username'), 'password' : password,'token' : acces_token})
        
        return response
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500

