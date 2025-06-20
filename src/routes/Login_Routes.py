from flask import Blueprint, make_response, request, jsonify
from flask_wtf import csrf
from src.services.admin_service import AdminService
from flask_jwt_extended import create_access_token
from flask_bcrypt import Bcrypt

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

@auth.route('/login', methods=['POST'])
def login_admin():
    try:
        if not request.json or 'username' not in request.json or 'password' not in request.json:
            return jsonify({'mensaje': 'La solicitud JSON debe incluir "username" y "password"'}), 400

        username = request.json['username']
        password = request.json['password']

        admin = AdminService.get_admin_by_username(username)

        print(admin)

        if not admin:
            return jsonify({'mensaje': 'El admin no existe'}), 404

        pw_hash = admin.get('password')
        
        if not bcrypt.check_password_hash(pw_hash, password):
            return jsonify({'mensaje': 'Contraseña incorrecta'}), 401

        acces_token = create_access_token(identity=username)

        response = jsonify({'id' : admin.get('id'), 'username':admin.get('username'),'token' : acces_token})
        
        return response
    except Exception as ex:
        return jsonify({'mensaje': f'Error interno del servidor: {str(ex)}'}), 500


@auth.route('/csrf-token', methods=['GET'])
def get_csrf_token():
    token = csrf.generate_csrf()  
    resp = make_response(jsonify({'csrf_token': token}))
    resp.set_cookie('csrf_token', token, httponly=False, samesite='None', secure=True)
    return resp

