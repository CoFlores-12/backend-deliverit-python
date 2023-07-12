from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os
import json

load_dotenv()

USR = os.getenv("USR")
PW = os.getenv("PW")

uri = "mongodb+srv://"+USR+":"+PW+"@deliverit.elvsi2t.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

mydb = client["test"]
mycol = mydb["clients"]
fd =  mycol.find_one({"email": "cofloresf@unah.hn"})
print(fd["password"])
