from flask import Flask
from flask_pymongo import PyMongo
import os

######  RETURNS THE MONGO DB COLLECTION FROM THE DB  #######

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://keimo:keimo123@ds141924.mlab.com:41924/blog-db"
mongo = PyMongo(app)

def get_mongo_collection(CollectionName):
    return mongo.db[CollectionName]

######   END OF THE UTIL TO GET COLLECTION FROM DB   #######

def get_app_base_path():
    return os.path.dirname(os.path.realpath(__file__))

def get_instance_folder_path():
    return os.path.join(get_app_base_path(), 'instance')