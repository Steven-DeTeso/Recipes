from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import bcrypt
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_user_register(form_data:dict[str, str]) -> bool:
        is_valid = True
        is_valid_email = True

        if len(form_data.get('first_name')) <= 2:
            flash("First name has to be longer and/or not blank!", 'register')
            is_valid = False
        if len(form_data.get('last_name')) < 2:
            flash("Last name has to be longer and/or not blank!", 'register')
            is_valid = False
        if len(form_data.get('email')) <= 0:
            flash("A valid email is required!", 'register')
            is_valid = False
            is_valid_email = False
        if not EMAIL_REGEX.match(form_data.get('email')):
            flash("The email you entered is in the wrong format!  ----------- Use this example format ----------- <email-name>@<service>.<something>", 'register')
            is_valid = False
            is_valid_email = False
        if is_valid_email:
            query = "SELECT * FROM users WHERE email = %(email)s;"
            result = connectToMySQL('recipe_schema').query_db(query, form_data)
            if len(result) >= 1:
                flash("Email is already registered in system!", 'register')
                is_valid = False
        if len(form_data.get('password')) < 8:
            flash("Your password isn't long enough! It has to be at least 8 characters!", 'register')
            is_valid = False
        if form_data.get('password') != form_data.get('confirm_password'):
            flash('Passwords must match!', 'register')
            is_valid = False
        if form_data.get('radio') != 'verified':
            flash('Please verify you are NOT a robot!', 'register')
            is_valid = False
        
        return is_valid

    @staticmethod
    def validate_user_login(form_data:dict) -> bool:
        is_valid = True
        is_valid_email = True
        
        if len(form_data.get('email')) <= 0:
            flash("A valid email is required!", 'login')
            is_valid = False
            is_valid_email = False
        if not EMAIL_REGEX.match(form_data.get('email')):
            flash("The email you entered is in the wrong format!  ----------- Use this example format ----------- <email-name>@<service>.<something>", 'login')
            is_valid = False
            is_valid_email = False
        if is_valid_email:
            query = "SELECT * FROM users WHERE email = %(email)s;"
            result = connectToMySQL('recipe_schema').query_db(query, form_data)
            if not bcrypt.check_password_hash(result[0]['password'], form_data.get('password')):
                flash('Invalid Password entered', 'login')
                is_valid = False
                
        return is_valid

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());
        """
        return connectToMySQL('recipe_schema').query_db(query, data)
    
    @classmethod
    def get_user_by_email(cls, data:dict):
        query = """
        SELECT * 
        FROM users 
        WHERE email = %(email)s;
        """
        result = connectToMySQL('recipe_schema').query_db(query, data)
        if len(result) < 1: 
            return False
        return cls(result[0])

    @classmethod 
    def get_user_by_id(cls, data):
        query = """
        SELECT * 
        FROM users 
        WHERE id = %(id)s;
        """
        result = connectToMySQL('recipe_schema').query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_one_for_login(cls, data):
        query = """
        SELECT * 
        FROM users
        WHERE email = %(email)s
        """
        return connectToMySQL('recipe_schema').query_db(query, data)