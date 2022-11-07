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

@app.route('/recipe/view/<int:id>')
def r_recipes_view(id):
    return render_template('recipes_view.html', recipe = Recipe.get_one({'id':id}))

@app.route('/recipe/edit/<int:id>')
def r_recipes_edit(id):
    return render_template('recipes_edit.html', recipe = Recipe.get_one({'id':id}))

@app.route('/recipe/redo', methods=['POST'])
def f_recipes_redo_update():
    Recipe.update_recipe(request.form)
    return redirect('/login/success')

@app.route('/recipe/delete/<int:id>')
def rd_recipes_delete(id):
    Recipe.delete_recipe({'id':id})
    return redirect('/login/success')
