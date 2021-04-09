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
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

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

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
