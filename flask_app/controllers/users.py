from flask_app import app, bcrypt
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask import render_template, request, redirect, session

@app.route('/')
def r_home_page():
    return render_template('index.html')

@app.route('/register/user', methods=['POST'])
def f_register_user():
    if User.validate_user_register(request.form):
        data = {
        'first_name': request.form.get('first_name'),
        'last_name': request.form.get('last_name'),
        'email': request.form.get('email'),
        'password': bcrypt.generate_password_hash(request.form.get('password'))
        }
        User.save(data)
        user_in_db = User.get_one_for_login(data)
        session['user_data'] = {
            'id': user_in_db[0]['id'], #steps in to just grab dict:object from list,hench [0]
            'first_name': user_in_db[0]['first_name'],
            'last_name': user_in_db[0]['last_name']
        }

        return redirect('/login/success')
    return redirect('/')

@app.route('/login/user', methods=['POST'])
def f_login_user():
    if not User.validate_user_login(request.form):
        return redirect('/')
    data = {
        'email': request.form.get('email')
    }
    user_in_db = User.get_one_for_login(data)
    session['user_data'] = user_in_db[0]
    return redirect('/login/success')

@app.route('/login/success')
def r_success():
    recipes = Recipe.get_all_recipes()
    if 'user_data' not in session:
        return redirect('/log_out')
    return render_template('dashboard.html', user = session['user_data'], recipes = recipes)

@app.route('/log_out')
def rd_log_out():
    session.clear()
    return redirect('/')