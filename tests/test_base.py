from flask import current_app, url_for
from flask_testing import TestCase

from main import app

class MainTest(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False

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
    
    def test_hello_post(self):
        fake_form = {
            'email': 'fake',
            'password': 'fake-password',
        }
        response = self.client.post(url_for('auth.login'), data=fake_form)
        self.assertRedirects(response, url_for('profile.home'))