from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import json
from bson import json_util
from bson.objectid import ObjectId

load_dotenv()

USR = os.getenv("USR")
PW = os.getenv("PW")

app = Flask(__name__)
app.run(port=3000,debug=True)

uri = "mongodb+srv://"+USR+":"+PW+"@deliverit.elvsi2t.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

mydb = client["test"]

@app.route("/login", methods=['POST'])
def login():
    data = request.json
    if len(str(data.get('email'))) > 0:
        mycol = mydb["clients"]
        fd =  mycol.find_one({ "email": str(data.get('email'))})
        if fd:
            if data.get('password')==fd['password']:
                return str(fd)
            else:
                return "Error Pass"
        else:
            return "Error User"
    return "Error"

@app.route("/signin", methods=['POST'])
def sigin():
    data = request.json
    if len(str(data.get('email'))) != 0 or len(str(data.get('username'))) != 0 or len(str(data.get('password'))) != 0:
        mycol = mydb["clients"]
        fd =  mycol.find_one({ "email": str(data.get('email'))})

        if fd:
            return "user already exists"

        data = {
            "username": str(data.get('username')),
            "email": str(data.get('email')),
            "password": str(data.get('password'))
        }

        x = mycol.insert_one(data)
        return "Inserted"
    return "Error"

@app.route("/categories", methods=['GET'])
def categories():
    mycol = mydb["categories"]
    fd =  mycol.find()
    return json.loads(json_util.dumps(fd))

@app.route("/categories/<idCategory>", methods=['GET'])
def categoriesID(idCategory):
    if len(str(idCategory)) > 0:
        mycol = mydb["categories"]
        fd =  mycol.find({"_id": ObjectId(idCategory)})
        return json.loads(json_util.dumps(fd))
    return "Error"

@app.route("/stores/<idCategory>", methods=['GET'])
def storescategoriesID(idCategory):
    if len(str(idCategory)) > 0:
        mycol = mydb["stores"]
        fd =  mycol.find({"category.id": ObjectId(idCategory)})
        return json.loads(json_util.dumps(fd))
    return "Error"

@app.route("/store/<idStore>", methods=['GET'])
def storeID(idStore):
    if len(str(idStore)) > 0:
        mycol = mydb["stores"]
        fd =  mycol.find({"_id": ObjectId(idStore)})
        return json.loads(json_util.dumps(fd))
    return "Error"
