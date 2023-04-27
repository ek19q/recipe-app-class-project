# Eliza Knight
# Spring 2023
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

DB_NAME = "database.db"

# Confuguring the database
app.config['SECRET_KEY'] = 'you will never guess'
app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)    # Initializing the database

# Creating the database model
class Recipes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    servings = db.Column(db.String(10), nullable=False)
    ingredients = db.Column(db.String(100), nullable=False)
    instructions = db.Column(db.String(500), nullable=False)

    def __init__(self, name, servings, ingredients, instructions):
        self.name = name
        self.servings = servings
        self.ingredients = ingredients
        self.instructions = instructions

# Creating the database
with app.app_context():
    db.create_all()

# Creating the routes
@app.route('/')
def index():
    recipe_data = db.session.query(Recipes) # Getting all the data from the database
    return render_template('index.html', data=recipe_data)  # Passing the data to the template

@app.route('/input', methods=['GET', 'POST'])   
def input_data():

    # Getting the data from the form
    if request.method == 'POST':
        name = request.form['name']
        servings = request.form['servings']
        ingredients = request.form['ingredients']
        instructions = request.form['instructions']

        add_data = Recipes(name, servings, ingredients, instructions)
        
        # Adding the data to the database
        db.session.add(add_data)
        db.session.commit()

        # Flashing a message
        flash("Recipe Added Successfully!!")
        logging.info("Recipe Created")

        return redirect(url_for('index'))   # Redirecting to the index page

    return render_template('input.html')    # Rendering the home page template

@app.route('/edit/<int:id>')    
def edit_data(id):
    recipe_data = Recipes.query.get(id)     # Getting the data for specific id from the database
    return render_template('edit.html', data=recipe_data)

@app.route('/save_edit', methods=['POST', 'GET'])
def save_edit():
    recipe_data = Recipes.query.get(request.form.get('id'))  # Getting the data for specific id from the form

    recipe_data.name = request.form['name']
    recipe_data.servings = request.form['servings']
    recipe_data.ingredients = request.form['ingredients']
    recipe_data.instructions = request.form['instructions']

    db.session.commit()

    flash('Recipe Edited Successfully!!')
    logging.info("Recipe Edited")

    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    recipe_data = Recipes.query.get(id)

    # Deleting the data from the database
    db.session.delete(recipe_data)
    db.session.commit()

    flash('Data Deleted Successfully.')
    logging.info("Recipe Deleted")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)   # Running the app in debug mode
