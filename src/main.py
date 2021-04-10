"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ.get('FLASK_APP_KEY') # Change this!
jwt = JWTManager(app)

# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if username != "test" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

####### USER FUNCTIONS #######

@app.route('/user', methods=['GET'])
def getAllUsers():
    all_users = User.query.all()
    all_users = list(map(lambda x: x.serialize(), all_users))
    return jsonify(all_users), 200

@app.route('/user/<int:id>', methods=['GET'])
def getSingleUser(id):
    user = User.query.get(id)
    return jsonify(user.serialize()), 200

@app.route('/user', methods=['POST'])
def createUser():
    body = request.get_json()
    user = User(username=body["username"], email=body["email"], name=body["name"], lastname=body["lastname"], password=body["password"])
    db.session.add(user)
    db.session.commit()
    print("User has been created!", body)
    return jsonify(body), 200

@app.route('/user/<int:id>', methods=['PUT'])
def updateUser(id):
    body = request.get_json()
    userToUpdate = User.query.get(id)
    if userToUpdate is None:
        raise APIException('User not found', status_code=404)

    if "username" in body:
        userToUpdate.username = body["username"]
    if "name" in body:
        userToUpdate.name = body["name"]
    if "lastname" in body:
        userToUpdate.lastname = body["lastname"]
    if "email" in body:
        userToUpdate.email = body["email"]
    db.session.commit()
    return("User has been updated correctly!")

@app.route('/user/<int:id>', methods=['DELETE'])
def deleteUsers(id):
    user = User.query.get(id)
    if user is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(user)
    db.session.commit()
    return("The user has been deleted")

####### USER FUNCTIONS #######

####### PLANET FUNCTIONS #######

@app.route('/planet', methods=['GET'])
def getAllPlanets():
    all_planets = Planet.query.all()
    all_planets = list(map(lambda x: x.serialize(), all_planets))
    return jsonify(all_planets), 200

@app.route('/planet/<int:id>', methods=['GET'])
def getSinglePlanet(id):
    planet = Planet.query.get(id)
    return jsonify(planet.serialize()), 200

@app.route('/planet', methods=['POST'])
def createPlanet():
    body = request.get_json()
    planet = Planet(name=body["name"], population=body["population"], capital=body["capital"])
    db.session.add(planet)
    db.session.commit()
    print("Planet has been created!", body)
    return jsonify(body), 200

@app.route('/planet/<int:id>', methods=['PUT'])
def updatePlanet(id):
    body = request.get_json()
    planetToUpdate = Planet.query.get(id)
    if planetToUpdate is None:
        raise APIException('User not found', status_code=404)

    if "name" in body:
        planetToUpdate.name = body["name"]
    if "population" in body:
        planetToUpdate.population = body["population"]
    if "capital" in body:
        planetToUpdate.capital = body["capital"]
    db.session.commit()
    return("Planet has been updated correctly!")

@app.route('/planet/<int:id>', methods=['DELETE'])
def deletePlanets(id):
    planet = Planets.query.get(id)
    if planet is None:
        raise APIException('Planet not found', status_code=404)
    db.session.delete(planet)
    db.session.commit()
    return("The planet has been deleted")

####### CHARACTER FUNCTIONS #######

@app.route('/character', methods=['GET'])
def getAllCharacters():
    all_characters = Character.query.all()
    all_characters = list(map(lambda x: x.serialize(), all_characters))
    return jsonify(all_characters), 200

@app.route('/character/<int:id>', methods=['GET'])
def getSingleCharacter(id):
    character = Character.query.get(id)
    return jsonify(character.serialize()), 200

@app.route('/character', methods=['POST'])
def createCharacter():
    body = request.get_json()
    character = Character(name=body["name"], lastname=body["lastname"], age=body["age"], ship=body["ship"])
    db.session.add(character)
    db.session.commit()
    print("Character has been created!", body)
    return jsonify(body), 200

@app.route('/character/<int:id>', methods=['PUT'])
def updateCharacter(id):
    body = request.get_json()
    characterToUpdate = Planet.query.get(id)
    if characterToUpdate is None:
        raise APIException('Character not found', status_code=404)

    if "name" in body:
        characterToUpdate.name = body["name"]
    if "lastname" in body:
        characterToUpdate.lastname = body["lastname"]
    if "age" in body:
        characterToUpdate.age = body["age"]
    if "ship" in body:
        characterToUpdate.ship = body["ship"]
    db.session.commit()
    return("Character has been updated correctly!")

@app.route('/character/<int:id>', methods=['DELETE'])
def deleteCharacters(id):
    character = Character.query.get(id)
    if character is None:
        raise APIException('Character not found', status_code=404)
    db.session.delete(character)
    db.session.commit()
    return("The character has been deleted")
    
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
