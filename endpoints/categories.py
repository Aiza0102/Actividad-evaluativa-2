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
    """Verifica si el token proporcionado es válido."""
    return token == VALID_TOKEN

class CategoriesResource(Resource):
    def __init__(self):
        """Inicialización de la clase."""
        self.db = DatabaseConnection('db.json')
        self.db.connect()
        self.categories_data = self.db.get_categories()
        self.parser = reqparse.RequestParser()

    def get(self, category_id=None):
        """Obtiene una categoría o todas las categorías disponibles."""
        token = request.headers.get('Authorization')

        if not token or not is_valid_token(token):
            return jsonify({'message': 'Unauthorized, invalid or missing token'}), 401

        if category_id:
            category = next((cat for cat in self.categories_data if cat['id'] == category_id), None)
            if category:
                return jsonify(category)
            return jsonify({'message': 'Category not found'}), 404

        return jsonify(self.categories_data), 200

    def post(self):
        """Agrega una nueva categoría."""
        token = request.headers.get('Authorization')

        if not token or not is_valid_token(token):
            return jsonify({'message': 'Unauthorized, invalid or missing token'}), 401

        self.parser.add_argument('name', type=str, required=True, help='Name of the category')
        args = self.parser.parse_args()

        if any(cat['name'] == args['name'] for cat in self.categories_data):
            return jsonify({'message': 'Category already exists'}), 400

        new_category = {'id': len(self.categories_data) + 1, 'name': args['name']}
        self.categories_data.append(new_category)
        self.db.add_category(new_category)

        return jsonify({'message': 'Category added successfully'}), 201

    def delete(self):
        """Elimina una categoría."""
        token = request.headers.get('Authorization')

        if not token or not is_valid_token(token):
            return jsonify({'message': 'Unauthorized, invalid or missing token'}), 401

        self.parser.add_argument('name', type=str, required=True, help='Name of the category')
        args = self.parser.parse_args()

        category_to_remove = next((cat for cat in self.categories_data if cat['name'] == args['name']), None)
        if not category_to_remove:
            return jsonify({'message': 'Category not found'}), 404

        self.categories_data = [cat for cat in self.categories_data if cat['name'] != args['name']]
        self.db.remove_category(args['name'])

        return jsonify({'message': 'Category removed successfully'}), 200