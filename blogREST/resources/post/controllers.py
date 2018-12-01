from flask import Blueprint
from flask_restful import Resource
from blogREST.models import user


class postInfo(Resource):
    def get(self):
        usr = user.User(email = 'test2@a.a',password="asdasda" )
        usr.save()
        return {'task': 'Say "Hello, World!"'}
