import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Person, Quote

DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')  
DB_USER = os.getenv('DB_USER', 'mohamed')  
DB_NAME = os.getenv('DB_NAME', 'quotation')
admin_token_v = os.environ['admin_JWT']

class QuotationTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path_local = "postgresql://{}@{}/{}".format(DB_USER, DB_HOST, DB_NAME)
        self.database_path_heroku = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path_local)

        self.admin_token = "Bearer {}".format(admin_token_v)
        # print(self.admin_token)
        self.new_person = {
            'name': 'Mohamed'
        }

        self.new_person_not_valid = {
            'name': None
        }

        self.new_quote = {
            'title': 'Do',
            'description': 'Do what you have to do',
            'person_id': 1
        }

        self.new_quote_not_valid = {
            'title': 'Do',
            'description': 'Do what you have to do'
        }
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_create_new_person(self):
        res = self.client().post('/persons', json=self.new_person, headers={
            'Content-Type': 'application/json',
            'Authorization': self.admin_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['persons'])
        self.assertTrue(data['total_persons'])
    
    def test_create_new_quote(self):
        res = self.client().post('/quotes', json=self.new_quote, headers={
            'Content-Type': 'application/json',
            'Authorization': self.admin_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['quotes'])
        self.assertTrue(data['total_quotes'])
    
    def test_create_new_person_fail(self):
        res = self.client().post('/persons', json=self.new_person_not_valid, headers={
            'Content-Type': 'application/json',
            'Authorization': self.admin_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')
    
    def test_create_new_quote_fail(self):
        res = self.client().post('/quotes', json=self.new_quote_not_valid, headers={
            'Content-Type': 'application/json',
            'Authorization': self.admin_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'Unprocessable')
    
    def test_get_persons(self):
        res = self.client().get('/persons', headers={
            'Content-Type': 'application/json',
            'Authorization': self.admin_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_persons'])
        self.assertTrue(len(data['persons']))
    
    def test_get_quotes(self):
        res = self.client().get('/quotes', headers={
            'Content-Type': 'application/json',
            'Authorization': self.admin_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_quotes'])
        self.assertTrue(data['quotes'])
    
    def test_get_persons_fail(self):
        res = self.client().get('/personss', headers={
            'Content-Type': 'application/json',
            'Authorization': self.admin_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_get_quotes_fail(self):
        res = self.client().get('/quotess', headers={
            'Content-Type': 'application/json',
            'Authorization': self.admin_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_edit_person(self):
        res = self.client().patch(
            '/persons/1',
            json={
                'name': 'Salah'}, headers={
            'Content-Type': 'application/json',
            'Authorization': self.admin_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['person_id'])

    def test_edit_quote(self):
        res = self.client().patch(
            '/quotes/1',
            json={
                'title': 'Do somethingelse'}, headers={
            'Content-Type': 'application/json',
            'Authorization': self.admin_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['quote_id'])
    
    def test_edit_person_fail(self):
        res = self.client().patch(
            '/persons/99999',
            json={
                'name': 'Salah'}, headers={
            'Content-Type': 'application/json',
            'Authorization': self.admin_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_edit_quote_fail(self):
        res = self.client().patch(
            '/quotes/99999',
            json={
                'title': 'Do somethingelse'}, headers={
            'Content-Type': 'application/json',
            'Authorization': self.admin_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')
    

    def test_delete_qoute(self):
        res = self.client().delete('/quotes/1', headers={
            'Content-Type': 'application/json',
            'Authorization': self.admin_token
            })
        data = json.loads(res.data)

        quote = Quote.query.filter(Quote.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], self.id_delete)
        self.assertEqual(quote, None)
    
    def test_delete_person(self):
        res = self.client().delete('/persons/1', headers={
            'Content-Type': 'application/json',
            'Authorization': self.admin_token
            })
        data = json.loads(res.data)

        person = Person.query.filter(Person.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], self.p_id_delete)
        self.assertEqual(person, None) 
        
        
    def test_delete_qoute(self):
        res = self.client().delete('/quotes/9999999', headers={
            'Content-Type': 'application/json',
            'Authorization': self.admin_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')
    
    def test_delete_person(self):
        res = self.client().delete('/persons/99999999', headers={
            'Content-Type': 'application/json',
            'Authorization': self.admin_token
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found') 

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()