from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
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
    def get_all_recipes(cls):
        query = """
        SELECT * 
        FROM recipes
        JOIN users
        ON recipes.user_id = users.id;
        """
        results = connectToMySQL('recipes').query_db(query)
        recipes = []
        for recipe in results:
            one_recipe = cls(recipe)
            print(recipe)
            data = {
                'id':recipe['users.id'],
                'first_name': recipe['first_name'],
                'last_name': recipe['last_name'],
                'email': recipe['email'],
                'created_at': recipe['users.created_at'],
                'updated_at': recipe['users.updated_at']
            }
            one_recipe.user = User(data)
            recipes.append(one_recipe)
        return recipes

    @classmethod
    def get_one(cls, data):
        query = """
        SELECT *
        FROM recipes
        JOIN users on recipes.user_id = users.id 
        WHERE recipes.id = %(id)s;
        """
        result = connectToMySQL('recipes').query_db(query, data)
        only_recipe = cls(result[0])
        only_recipe.user = result[0]['first_name']
        return only_recipe

    @classmethod
    def update_recipe(cls, data):
        query = """
        UPDATE recipes 
        SET name = %(name)s, description = %(description)s,
        instruction = %(instruction)s, minute = %(minute)s,
        updated_at = NOW()
        WHERE id = %(id)s;
        """
        return connectToMySQL('recipes').query_db(query, data)

    @classmethod
    def delete_recipe(cls, data):
        query = """
        DELETE FROM recipes
        WHERE id = %(id)s;
        """
        return connectToMySQL('recipes').query_db(query, data)