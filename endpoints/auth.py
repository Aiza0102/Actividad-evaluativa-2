import os
from flask import Blueprint, request, jsonify
from flask_restful import Resource
from werkzeug.security import safe_str_cmp
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

# Usar variables de entorno
VALID_TOKEN = os.getenv('VALID_TOKEN')

def authenticate_user(username, password):
    """Simula la validación de un usuario con su nombre de usuario y contraseña."""
    if username == 'student' and password == 'desingp':
        return True
    return False

class AuthenticationResource(Resource):
    def post(self):
        """Autenticación de usuario y generación de token."""
        username = request.json.get('username')
        password = request.json.get('password')

        if not username or not password:
            return jsonify({'message': 'Missing username or password'}), 400

        if authenticate_user(username, password):
            token = VALID_TOKEN
            return jsonify({'token': token}), 200

        return jsonify({'message': 'Unauthorized'}), 401