import uuid
import hashlib
from flask import Flask,request, current_app,  Blueprint
from flask_restplus import Resource, Api, fields
from flask_pymongo import PyMongo
import os
import jwt


# from blogREST.models.user import User



util = Blueprint('util',__name__)
api = Api(util)




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

# required_token decorator
def token_required(f):
    userCollection = get_mongo_collection('User')
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        current_user = None
        if auth_header:
            try:
                access_token = auth_header.split(' ')[1]

                try:
                    token = jwt.decode(access_token, current_app.config['SECRET_KEY'])
                    current_user = userCollection.find_one({"uid":token['uid']})
                except jwt.ExpiredSignatureError as e:
                    raise e
                except (jwt.DecodeError, jwt.InvalidTokenError) as e:
                    raise e
                except:
                    api.abort(401, 'Unknown token error')

            except IndexError:
                raise jwt.InvalidTokenError
        else:
            api.abort(403, 'Token required')
        return f(*args, **kwargs, current_user=current_user)

    wrapper.__doc__ = f.__doc__
    wrapper.__name__ = f.__name__
    return wrapper