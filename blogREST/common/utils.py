import uuid
import hashlib
from flask import Flask
from flask_pymongo import PyMongo
import os

######  RETURNS THE MONGO DB COLLECTION FROM THE DB  #######

app = Flask(__name__)
app.config["MONGO_URI"] = os.getenv('mongourl')
mongo = PyMongo(app)


def get_mongo_collection(CollectionName):
    return mongo.db[CollectionName]

######   END OF THE UTIL TO GET COLLECTION FROM DB   #######


def get_app_base_path():
    return os.path.dirname(os.path.realpath(__file__))


def get_instance_folder_path():
    return os.path.join(get_app_base_path(), 'instance')


def hash_password(password):
    # uuid is used to generate a random number
    salt = uuid.uuid4().hex
    return hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return password == hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()
