import unittest
from flask import Flask
from app import input_data



class TestInputData(unittest.TestCase):
    
    def setUp(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        self.app = app.test_client()
        
    def test_input_data(self):
        with self.app as client:
            data = {'name': 'Pasta', 'servings': '4', 'ingredients': 'pasta, tomato sauce', 'instructions': 'cook pasta, mix with tomato sauce'}
            response = client.post('/input', data=data, follow_redirects=False)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Recipe Added Successfully!!", response.data)
            