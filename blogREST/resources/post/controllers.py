from flask import Blueprint
from flask_restful import Resource


class postInfo(Resource):
    def get(self):
        return {'task': 'Say "Hello, World!"'}
