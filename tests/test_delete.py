import unittest
from flask import Flask
from app import delete, db, Recipes


class TestDelete(unittest.TestCase):
    
    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.init_app(app)
        with app.app_context():
            db.create_all()
        self.app = app.test_client()
        self.recipe = Recipes(name='Test Recipe', servings=4, ingredients='eggs, cheese', instructions='cook eggs, add cheese')
        with app.app_context():
            db.session.add(self.recipe)
            db.session.commit()
        
    def test_delete(self):
        with self.app as client:
            response = client.get(f'/delete/{self.recipe.id}', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Data Deleted Successfully.", response.data)
            with self.assertRaises(AttributeError):
                # Trying to access the recipe data after it's been deleted should raise an AttributeError
                self.recipe.name
            
