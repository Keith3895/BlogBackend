####### STANDARD/INSTALLED PACKAGES #######
from flask import Flask, Blueprint, jsonify, redirect, url_for, session
from flask_restplus import Resource, Api, fields
from flask_pymongo import PyMongo

####### USER DEFINED PACKAGES #######
from blogREST.models.user import User
from blogREST.models.api_model.user import get_user_model
from blogREST.common.utils import get_mongo_collection


user_blueprint = Blueprint('user',__name__)
api = Api(user_blueprint)

userCollection = get_mongo_collection('User')

user_model_for_POST = api.model('Register User', get_user_model('POST'))
user_model_for_GET = api.model('User Details', get_user_model('GET'))

UserData = {
    'email' : 'james@gmail.com',
    'password' : 'hello123',
    'first_name' : 'James',
    'last_name' : 'Hamilton'
}


@api.route('/list')
class List(Resource):
    # @api.doc('List users')
    # @api.marshal_with(user_model_for_GET)
    def get(self):
        if 'user_id' in session:
            return {'message' : 'You are logged in!'}
        # all_users = []
        # result = userCollection.find()
        # for user in result:
        #     all_users.append(user)
        # print(all_users)
        # return all_users
        else:
            return {'message' : 'You are not logged in!'}

    # @api.doc('Register User')
    @api.expect(user_model_for_POST)
    # @api.marshal_with(user_model_for_POST)
    def post(self):
        user_data = api.payload
        print(user_data)
        return userCollection.insert_one(user_data)
        # return userCollection.find_one()
