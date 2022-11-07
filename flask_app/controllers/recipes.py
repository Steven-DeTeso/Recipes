from flask_app import app
from flask_app.models.recipe import Recipe
from flask import render_template, request, redirect, session

@app.route('/recipes/new')
def r_recipes_new():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('recipes_new.html')

@app.route('/recipe/create', methods=['POST'])
def f_recipes_create():
    Recipe.save(request.form)
    return redirect('/login/success')
