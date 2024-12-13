import unittest
from app import app, db, User

class UserModelTest(unittest.TestCase):

    def setUp(self):
        # Configura una base de dades de prova
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Elimina la base de dades de prova
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_unique_email(self):
        with app.app_context():
            user1 = User(username="testuser1", name="TestName1", surname="Surname1", email="test1@example.com", password="1234", age=30)
            user2 = User(username="testuser2", name="TestName2", surname="Surname2", email="test1@example.com", password="5678", age=35)

            db.session.add(user1)
            db.session.commit()

            with self.assertRaises(Exception):  # Email duplicat
                db.session.add(user2)
                db.session.commit()

    def test_age_validation(self):
        with app.app_context():
            with self.assertRaises(ValueError):  # Edat inferior a 18
                User.validate_age(17)
            with self.assertRaises(ValueError):  # Edat superior a 120
                User.validate_age(121)

    def test_register_user(self):
        response = self.app.post('/register', data={
            'username': 'testuser',
            'name': 'TestName',
            'surname': 'testsurname',
            'email': 'test@example.com',
            'email2': 'test@example.com',
            'password': '1234',
            'age': 30
        })
        self.assertEqual(response.status_code, 302)  # Redirecció correcta després del registre


if __name__ == '__main__':
    unittest.main()
