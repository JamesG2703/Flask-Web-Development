from unittest import TestCase
from flask_login import login_fresh, login_required
from market import app, db
from market.models import User, Item
import unittest

class FlaskTestCase(unittest.TestCase):

    # Ensure there is a connection to the market database containing user and item data
    def test_create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
        return app

    # Ensure that Flask was set up correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/home', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure that Flask can load the home page correctly
    def test_home_page_loads(self):
        tester = app.test_client(self)
        response = tester.get('/home', content_type='html/text')
        self.assertTrue(b'Flask Stock Market' in response.data)
        self.assertTrue(b'Start Viewing the Stock Market by logging into your account' in response.data)
        self.assertTrue(b'Get Started' in response.data)
        self.assertTrue(b'Testing' not in response.data)

    # Ensure that Flask can load the login page and input credientials correctly
    def test_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(username='james', password='test12'),
            follow_redirects=True, content_type='html/text'
        )
        self.assertEqual(response.status_code, 200)

    # Ensure that Flask can load the login page and input credientials correctly
    def test_register(self):
        tester = app.test_client(self)
        response = tester.post(
            '/register',
            data=dict(username='james', email_address='test10@yahoo.com', password='test12'),
            follow_redirects=True, content_type='html/text'
        )
        self.assertEqual(response.status_code, 200)

    # Ensure that Flask can load the logout function
    def test_logout(self):
        tester = app.test_client(self)
        response = tester.get('/logout', follow_redirects=True, content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Start Viewing the Stock Market by logging into your account' in response.data)
        self.assertTrue(b'Get Started' in response.data)
        self.assertTrue(b'Testing' not in response.data)

    # Ensure that Flask can load the market page
    def test_market_loads(self):
        app.config['LOGIN_DISABLED'] = True
        tester = app.test_client(self)
        response = tester.get('/market', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Country Appeal Rate' in response.data)
        self.assertTrue(b'TestProduct' in response.data)
        self.assertTrue(b'123456321' in response.data)
        self.assertTrue(b'Testing Again' not in response.data)

    # # Ensure that Flask can load the edit item page
    # def test_edit_item_loads(self):
    #     app.config['LOGIN_DISABLED'] = True
    #     tester = app.test_client(self)
    #     response = tester.get('/edit_item/<int:id>', follow_redirects=True, content_type='html/text')
    #     self.assertEqual(response.status_code, 200
    #     self.assertTrue(b'Update Item' in response.data)

    # # Ensure that Flask can load the delete page
    # def test_delete_item_loads(self):
    #     app.config['LOGIN_DISABLED'] = True
    #     tester = app.test_client(self)
    #     response = tester.get('/delete_item/<int:id>', content_type='html/text')
    #     self.assertEqual(response.status_code, 200)

    # Ensure that Flask can load the live graphs page
    def test_live_graph_loads(self):
        app.config['LOGIN_DISABLED'] = True
        tester = app.test_client(self)
        response = tester.get('/live_graphs', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Return to stock market price page' in response.data)
        self.assertTrue(b'Testing once again' not in response.data)

    # # Ensure that Flask can load the graph page correctly
    # def test_graph_loads(self):
    #     app.config['LOGIN_DISABLED'] = True
    #     tester = app.test_client(self)
    #     response = tester.get('/graphs', content_type='html/text')
    #     self.assertEqual(response.status_code, 200)

    # Ensure that Flask can add new users to the database
    def test_userDB(self):
        db.create_all()
        db.session.add(User(username='TestUser', email_address='test2002@gmail.com', password_hash='test22'))
        db.session.commit()

    # Ensure that Flask can add new users to the database
    def test_itemDB(self):
        db.create_all()
        db.session.add(Item(name='TestProduct', country_appeal_rate='75%', category='Technology', price='150', barcode='123456321', description='This is a test'))
        db.session.commit()

    # Ensure that Flask can add delete data values from the database
    def test_deleteDB(self):
        db.session.remove()
        db.drop_all()

if __name__ == '__main__':
    unittest.main()