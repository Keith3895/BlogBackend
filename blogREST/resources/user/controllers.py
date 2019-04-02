####### STANDARD/INSTALLED PACKAGES #######
from flask import Flask, Blueprint, jsonify, redirect, url_for, session
from flask_restplus import Resource, Api, fields, Namespace
from flask_pymongo import PyMongo
import re


####### USER DEFINED PACKAGES #######
from blogREST.models.user import User
from blogREST.models.api_model.user import get_user_model
from blogREST.common.utils import get_mongo_collection
from blogREST.common.Exception import ValidationException
from blogREST.common.utils import hash_password
from blogREST.resources.auth.controllers import token_required
api = Namespace('user', description='Apis to perform user centeric actions.')

userCollection = get_mongo_collection('User')

user_model_for_POST = api.model('Register User', get_user_model('POST'))
user_model_for_GET = api.model('User Details', get_user_model('GET'))

UserData = {
    'email': 'james@gmail.com',
    'password': 'hello123',
    'first_name': 'James',
    'last_name': 'Hamilton'
}


@api.route('/list')
class List(Resource):
    @api.doc('List users')
    # @api.marshal_with(user_model_for_GET)
    def get(self):
        if 'user_id' in session:
            return {'message': 'You are logged in!'}
        # all_users = []
        # result = userCollection.find()
        # for user in result:
        #     all_users.append(user)
        # print(all_users)
        # return all_users
        else:
            return {'message': 'You are not logged in!'}

    # @api.doc('Register User')
    @api.expect(user_model_for_POST)
    # @api.marshal_with(user_model_for_POST)
    def post(self):
        user_data = api.payload
        print(user_data)
        return userCollection.insert_one(user_data)
        # return userCollection.find_one()


@api.route('/register')
class Register(Resource):

    # 4-16 symbols, can contain A-Z, a-z, 0-9, _ (_ can not be at the begin/end and can not go in a row (__))
    USERNAME_REGEXP = r'^(?![_])(?!.*[_]{2})[a-zA-Z0-9._]+(?<![_])$'

    # 6-64 symbols, required upper and lower case letters. Can contain !@#$%_  .
    PASSWORD_REGEXP = r'^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])[\w\d!@#$%_]{6,64}$'

    @api.expect(user_model_for_POST, validate=True)
    @api.marshal_with(user_model_for_POST)
    @api.response(400, 'username or password incorrect')
    def post(self):
        if not re.search(self.USERNAME_REGEXP, api.payload['username']):
            raise ValidationException(error_field_name='username',
                                      message='4-16 symbols, can contain A-Z, a-z, 0-9, _ \
                                      (_ can not be at the begin/end and can not go in a row (__))')

        if not re.search(self.PASSWORD_REGEXP, api.payload['password']):
            raise ValidationException(error_field_name='password',
                                      message='6-64 symbols, required upper and lower case letters. Can contain !@#$%_')

        # Check on Db if user exists
        if userCollection.find_one({"username": api.payload['username']}):
            raise ValidationException(
                error_field_name='username', message='This username is already exists')
        user = self.generateUserObject(api.payload)
        userCollection.insert_one(user)
        return user

    def generateUserObject(self, obj):
        import uuid
        userObj = obj
        userObj['password'] = hash_password(userObj['password'])
        userObj['uid'] = uuid.uuid4().hex
        return userObj
