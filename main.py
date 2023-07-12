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

@app.route("/", methods=['POST', 'GET'])
def hello_world():
    data = request.json
    return jsonify(data)