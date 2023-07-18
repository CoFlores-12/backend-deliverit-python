from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import json
from bson import json_util
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask_cors import CORS, cross_origin

load_dotenv()

USR = os.getenv("USR")
PW = os.getenv("PW")

app = Flask(__name__)
app.run(port=3000,debug=True)
CORS(app)
cors = CORS(app, resource={
    r"/*":{
        "origins":"*"
    }
})

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
    if request.form['email']:
        mycol = mydb["clients"]
        fd =  mycol.find_one({ "email": str(request.form['email'])})
        if fd:
            if str(request.form['password'])==fd['password']:
                return {
                    "username":fd['username'],
                    "_id":str(fd['_id'])
                }
            else:
                return "Error Pass"
        else:
            return "Error User"
    return "Error"

@app.route("/signin", methods=['POST'])
def sigin():
    if request.form['email'] or request.form['username'] or request.form['password']:
        mycol = mydb["clients"]
        fd =  mycol.find_one({ "email": str(request.form['email'])})

        if fd:
            return "user already exists"

        data = {
            "username": str(request.form['username']),
            "email": str(request.form['email']),
            "password": str(request.form['password'])
        }

        x = mycol.insert_one(data)
        return {
                    "username":str(request.form['username']),
                    "_id":str(x.inserted_id )
                }
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

@app.route("/CreateOrder", methods=['POST'])
def CreateOrder():
    if request.form['idClient']:
        mycol = mydb["orders"]
        fd =  mycol.find_one({ "_id": str(request.form['idClient'])})

        if fd:
            return "user already exists"

        data = {
            id: 1,
            status:  'Received',
            service: request.form['service'],
            total: request.form['total'],
            date: request.form['date'],
            payment: request.form['payment'],
            client:    {
                id: fd['_id'],
                name: fd['username'],
                email: fd['email']
            },
            dealer:     {
                id: null,
                name: null,
                email: null,
                tel: null
            },
            products: request.form['products'],
            locations: request.form['location']
        }

        x = mycol.insert_one(data)
        return x
    return "Error"