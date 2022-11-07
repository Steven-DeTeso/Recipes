from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.minute = data['minute']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO recipes (name, description, instruction, minute, created_at, updated_at, user_id)
        VALUES (%(name)s, %(description)s, %(instruction)s, %(minute)s, NOW(), NOW(), %(user_id)s);
        """
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def get_all_recipes(cls, data):
        query = """
        SELECT * 
        FROM recipes;
        """
        results = connectToMySQL('recipes').query_db(query, data)
        recipes = []
        for recipe in results:
            one_recipe = cls(recipe)
            one_recipe.user = recipe['name']
            recipes.append(one_recipe)
        return recipes
