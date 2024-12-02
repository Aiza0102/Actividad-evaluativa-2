import os
from flask_restful import Resource, reqparse
from flask import request, jsonify
from dotenv import load_dotenv
from utils.database_connection import DatabaseConnection

# Cargar variables desde .env
load_dotenv()

# Usar variables de entorno
VALID_TOKEN = os.getenv('VALID_TOKEN')

def is_valid_token(token):
    """Verifica si el token es válido."""
    return token == VALID_TOKEN

class FavoritesResource(Resource):
    def __init__(self):
        """Inicialización de la clase de favoritos."""
        self.db = DatabaseConnection('favorites.json')
        self.db.connect()
        self.favorites = self.db.get_favorites()

    def get(self):
        """Obtiene todos los productos favoritos."""
        token = request.headers.get('Authorization')

        if not token or not is_valid_token(token):
            return jsonify({'message': 'Unauthorized, invalid or missing token'}), 401

        return jsonify(self.db.get_favorites()), 200

    def post(self):
        """Agrega un producto a los favoritos."""
        token = request.headers.get('Authorization')

        if not token or not is_valid_token(token):
            return jsonify({'message': 'Unauthorized, invalid or missing token'}), 401

        # Validación de parámetros
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID')
        parser.add_argument('product_id', type=int, required=True, help='Product ID')
        args = parser.parse_args()

        if not args['user_id'] or not args['product_id']:
            return jsonify({'message': 'User ID and Product ID are required'}), 400

        # Crear nuevo favorito y guardarlo
        new_favorite = {'user_id': args['user_id'], 'product_id': args['product_id']}
        self.favorites.append(new_favorite)
        self.db.add_favorite(new_favorite)

        return jsonify({'message': 'Product added to favorites', 'favorite': new_favorite}), 201

    def delete(self):
        """Elimina un producto de los favoritos."""
        token = request.headers.get('Authorization')

        if not token or not is_valid_token(token):
            return jsonify({'message': 'Unauthorized, invalid or missing token'}), 401

        # Parseo de parámetros para eliminación
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID')
        parser.add_argument('product_id', type=int, required=True, help='Product ID')
        args = parser.parse_args()

        if not args['user_id'] or not args['product_id']:
            return jsonify({'message': 'User ID and Product ID are required'}), 400

        # Eliminar el favorito
        self.favorites = [favorite for favorite in self.favorites if not (
            favorite['user_id'] == args['user_id'] and favorite['product_id'] == args['product_id'])]
        self.db.save_favorites(self.favorites)

        return jsonify({'message': 'Product removed from favorites'}), 200