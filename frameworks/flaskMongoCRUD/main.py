from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask import Response 
from werkzeug.security import generate_password_hash
import json
import helpers


# Connecting to the docker mongo instance
app = Flask(__name__)

# /user is the database
app.config["MONGO_URI"] = "mongodb://localhost:27017/user"
mongodb = PyMongo(app)
db = mongodb.db


# route routes to url endpoints
@app.route("/")
def hello():
    return jsonify(
        message="The endpoints are /users, /users/<id>"
    )

@app.route("/users", methods=["GET"])
def showUserList():

    # userCRUD is the collection
    # find() finds all documents inside userCRUD collection
    users = db.userCRUD.find()
    data = []
    for user in users:
        item = {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
        }
        data.append(item)

    # returns a list as JSON
    return jsonify(data)

@app.route("/users", methods=["POST"])
def createUser():
    
    # Convert request.data bytecode to JSON
    content = json.loads(request.data)

    # Validate user input
    validUser = helpers.validateCreateUser(content)
    if not validUser:
        return Response(status=400)
    password = generate_password_hash(content["password"])
    user = {
        "name": content["name"],
        "email": content["email"],
        "password": password
    }

    # Insert the user into the DB
    db.userCRUD.insert_one(user)
    return Response(
        status=201
    )

@app.route("/users/<id>", methods=["PUT"])
def updateUser(id):
    content = json.loads(request.data)
    validUpdateUser = helpers.validateUpdateUser(content)
    
    if not validUpdateUser:
        return Response(
            status=400
        )
    
    # $set tells mongo to update, you would only have to pass specific keys that you want to update
    response = db.userCRUD.update_one(
        {"_id": ObjectId(id)},
        {"$set": content}
    )

    # If any documents got matched
    if response.matched_count:
        return Response(
            status=200
        )
    else:
        return Response(
            status=400
        )

@app.route("/users/<id>", methods=["GET"])
def showSpecificUser(id):
    user = db.userCRUD.find_one_or_404({"_id": ObjectId(id)})
    user["_id"] = str(user["_id"])
    del user["password"]
    return jsonify(
        user
    )

@app.route("/users/<id>", methods=["DELETE"])
def delUser(id):
    response = db.userCRUD.delete_one({"_id": ObjectId(id)})

    if response.deleted_count:
        return Response(
            status=200
        )
    else:
        return Response(
            status=404
        )