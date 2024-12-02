import json

class DatabaseConnection:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path
        self.data = None

    def connect(self):
        try:
            with open(self.json_file_path, 'r') as json_file:
                self.data = json.load(json_file)
        except FileNotFoundError:
            self.data = {'products': [], 'categories': [], 'favorites': []}
            print("Error: Database file not found, creating a new one.")
            self.save_data()

    def save_data(self):
        with open(self.json_file_path, 'w') as json_file:
            json.dump(self.data, json_file, indent=4)

    def get_products(self):
        return self.data.get('products', [])

    def get_categories(self):
        return self.data.get('categories', [])

    def get_favorites(self):
        return self.data.get('favorites', [])

    def add_product(self, product):
        self.data['products'].append(product)
        self.save_data()

    def add_category(self, category):
        self.data['categories'].append(category)
        self.save_data()

    def add_favorite(self, favorite):
        self.data['favorites'].append(favorite)
        self.save_data()

    def remove_category(self, category_name):
        self.data['categories'] = [cat for cat in self.data['categories'] if cat["name"] != category_name]
        self.save_data()

    def save_favorites(self, favorites):
        self.data['favorites'] = favorites
        self.save_data()