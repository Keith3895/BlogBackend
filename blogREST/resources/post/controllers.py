from flask import Flask, Blueprint, jsonify, redirect, url_for, session
from flask_restplus import Resource, Api, fields
from flask_pymongo import PyMongo
from bson.json_util import dumps


from blogREST.models.post import Post
from blogREST.common.utils import get_mongo_collection
from blogREST.models.api_model.post import get_post_model

postInfo_blueprint = Blueprint('post',__name__)

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}


api = Api(postInfo_blueprint,authorizations=authorizations)

postCollection = get_mongo_collection('Post')
@api.doc('Blog Post')
@api.route('/blog')
class postInfo(Resource):
    postReqModel = api.model('Add New Blog Post', get_post_model('POST'))
    
    '''
        Get Request Defnitions.
    '''
    def get(self):
        return dumps(postCollection.find({}))



    @api.marshal_with(postReqModel)
    @api.header('application/json')
    @api.doc(security='apikey')
    def post(self):
        print(api.payload)
        postContent = api.payload
        temp = postCollection.find({})
        postCollection.insert_one(postContent)
        return temp