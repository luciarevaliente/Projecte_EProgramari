# Defineix les taules de la base de dades amb SQLAlchemy, basant-se en el disseny relacional.
# FER DISSENY RELACIONAL I ER
from . import db

# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), nullable=False, unique=True)
#     email = db.Column(db.String(100), nullable=False, unique=True)
#     role = db.Column(db.Enum('senior', 'family', 'medical', 'volunteer'), nullable=False)
#     registration_date = db.Column(db.DateTime, default=db.func.now())

# class SocialNetwork(db.Model):
#     __tablename__ = 'social_networks'
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     creation_date = db.Column(db.DateTime, default=db.func.now())
#     members = db.relationship('User', secondary='network_members', backref='networks')

# network_members = db.Table(
#     'network_members',
#     db.Column('network_id', db.Integer, db.ForeignKey('social_networks.id'), primary_key=True),
#     db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True)
# )
