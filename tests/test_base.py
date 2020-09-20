from flask import current_app, url_for
from flask_testing import TestCase

from main import app
from app.models import db

class MainTest(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sebastian:supertiancho99@localhost/scouting'

        return app

    def test_app_exists(self):
        self.assertIsNotNone(current_app)
    
    def test_app_in_test_mode(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_index_redirect(self):
        response = self.client.get(url_for('index'))
        print(response)
        self.assertRedirects(response, url_for('auth.login'))

    def test_login_get(self):
        response = self.client.get(url_for('auth.login'))
        self.assert200(response)

    def test_db(self):
        db.engine.execute('SELECT 1')
    
        