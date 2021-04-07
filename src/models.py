from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    # def __repr__(self):
    #     return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "name": self.name,
            "lastname": self.lastname,
            # do not serialize the password, its a security breach
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250), nullable = False)
    population = db.Column(db.Integer)
    capital = db.Column(db.String(250))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "capital": self.capital,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(250), nullable = False)
    lastname = db.Column(db.String(250))
    age = db.Column(db.Integer)
    ship = db.Column(db.String(250))

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "age": self.age,
            "ship": self.ship,
            # do not serialize the password, its a security breach
        }