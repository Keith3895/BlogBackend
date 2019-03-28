from flask import Flask, Blueprint, jsonify, redirect, url_for, session
from flask_restplus import Resource, Api, fields,Namespace
from flask_pymongo import PyMongo
from bson.json_util import dumps

from blogREST.resources.auth.controllers import token_required

from blogREST.models.post import Post
from blogREST.common.utils import get_mongo_collection
from blogREST.models.api_model.post import get_post_model



authorizations = {
    'apikey': {
        'type': 'token',
        'in': 'header',
        'name': 'Authorization'
    }
}

api = Namespace('post', description='Blog post related apis.',authorizations=authorizations)
# api = Api(postInfo_blueprint,)

postCollection = get_mongo_collection('Post')
@api.doc('Blog Post')
@api.route('/blog')
class postInfo(Resource):
    
    postReqModel = api.model('Add New Blog Post', get_post_model('POST'))
    
    '''
        Get Request Defnitions.
    '''
    @token_required
    def get(self):
        return dumps(postCollection.find({}))



    @api.marshal_with(postReqModel)
    @api.header('application/json')
    @api.doc(security='apikey')
    @token_required
    def post(self):
        print(api.payload)
        postContent = api.payload
        temp = postCollection.find({})
        postCollection.insert_one(postContent)
        return temp