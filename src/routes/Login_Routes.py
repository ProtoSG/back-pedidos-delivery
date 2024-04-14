from flask import Blueprint, request, jsonify
from src.services.admin_service import Admin_Service
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt

login = Blueprint('login', __name__)
bcrypt = Bcrypt()

@login.route('/login', methods=['POST'])
def login_admin():
    try:
        username = request.json['username']
        password = request.json['password']

        admin = Admin_Service.get_admin_by_username(username)
        pw_hash=''
        if(admin):
            pw_hash = admin.get('password')
        if not admin:
            return jsonify({'mensaje': 'El admin no existe'}), 404

        if not bcrypt.check_password_hash(pw_hash, password):
            return jsonify({'mensaje': 'Contraseña incorrecta'}), 401

        acces_token = create_access_token(identity=username)

        response = jsonify({'usernmae':admin.get('username'), 'token' : acces_token})
        response.set_cookie('token', value=acces_token, httponly=True, secure=False)
        
        return response
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500