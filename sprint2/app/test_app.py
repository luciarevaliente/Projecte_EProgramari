import unittest
from app import app, db, User, Appointment, MedicalRecord
from sqlalchemy.exc import IntegrityError

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register_user(self):
        response = self.app.post('/register', data={
            'username': 'testuser',
            'surname': 'testsurname',
            'email': 'test@example.com',
            'email2': 'test@example.com',
            'password': '1234',
            'age': 30
        })
        self.assertEqual(response.status_code, 302)
        with app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(user)

    def test_unique_email(self):
        with app.app_context():
            user1 = User(username="user1", surname="Surname1", email="test@example.com", password="1234", age=30)
            user2 = User(username="user2", surname="Surname2", email="test@example.com", password="5678", age=35)
            db.session.add(user1)
            db.session.commit()
            with self.assertRaises(IntegrityError):
                db.session.add(user2)
                db.session.commit()

    def test_age_validation(self):
        with self.assertRaises(ValueError):
            User.validate_age(17)
        with self.assertRaises(ValueError):
            User.validate_age(121)

if __name__ == '__main__':
    unittest.main()
