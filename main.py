from flask import Flask, request, jsonify
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

USR = os.getenv("USR")
PW = os.getenv("PW")

app = Flask(__name__)
app.run(debug=True)

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