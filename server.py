from flask_app import app
from flask_app.controllers import users, recipes
# from flask_app.controllers import <folder name> - folder name 
# won't be highlighted because we won't use it here, it will just be active

if __name__=="__main__":
    app.run(debug=True)