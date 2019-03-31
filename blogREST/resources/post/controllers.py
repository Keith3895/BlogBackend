from flask import Flask, Blueprint, jsonify, redirect, url_for, session
from flask_restplus import Resource, Api, fields, Namespace, reqparse
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

api = Namespace('post', description='Blog post related apis.',
                authorizations=authorizations)
# api = Api(postInfo_blueprint,)

postCollection = get_mongo_collection('Post')


@api.doc('Blog Post')
@api.route('/blog')
class postInfo(Resource):

    postReqModel = api.model('Add New Blog Post', get_post_model('POST'))
    postResModel = api.model('Add New Blog Post', get_post_model('GET'))

    '''
        Get Request Defnitions.
    '''
    @token_required
    def get(self):
        return dumps(postCollection.find({}))

    @api.marshal_with(postResModel)
    @api.header('application/json')
    @api.doc(security='apikey')
    @token_required
    def post(self, current_user):
        import uuid
        import datetime
        print(api.payload)

        postContent = api.payload
        postContent['slug'] = uuid.uuid4().hex
        postContent['user_id'] = current_user['uid']
        postContent['author'] = current_user['username']
        postContent['CreatDate'] = datetime.datetime.utcnow()
        # temp = postCollection.find({})
        postCollection.insert_one(postContent)
        return postContent


@api.route('/GetBlog/slug/<Slug>',
           '/GetBlog/title/<Title>')
class GetBlog(Resource):
    postResModel = api.model('Add New Blog Post', get_post_model('GET'))

    @api.marshal_with(postResModel)
    @api.header('application/json')
    def get(self, Slug=None, Title=None):
        '''
        Api call to get a specific blog Object.
        '''
        if Slug:
            findQuery = {'slug': Slug}
        elif Title:
            findQuery = {'title': Title}

        postResponse = postCollection.find_one(findQuery)
        return dumps(postResponse)


@api.route('/list/date/<date>/<pageNumber>',
           '/list/date/<fromDate>/<toDate>/<pageNumber>')
class ListByDate(Resource):
    postResModel = api.model('Add New Blog Post', get_post_model('GET'))
    project = {
        "$project":
        {
            "slug": 1,
            "title": 1,
            "author": 1,
            "CreatDate": 1,
            "content": {"$substr": ["$content", 0, 20]}
        }
    }
    limit =10
    
    @api.header('application/json')
    def get(self, date=None, fromDate=None, toDate=None,pageNumber=1):
        import datetime
        if date:
            match = {
                "$match": {
                    "CreatDate": {
                        "$gte": datetime.datetime.strptime(date, '%Y-%m-%d'),
                        "$lt": (datetime.datetime.strptime(date, '%Y-%m-%d')+datetime.timedelta(days=1))
                    }
                }
            }
        else:
            match = {
                "$match": {
                    "CreatDate": {
                        "$gte": datetime.datetime.strptime(fromDate, '%Y-%m-%d'),
                        "$lt": datetime.datetime.strptime(toDate, '%Y-%m-%d'),
                    }
                }
            }

        skips = self.limit * (pageNumber - 1)
        postsList = postCollection.aggregate([
            match,
            self.project,
            {"$skip":skips},
            {"$limit":self.limit}
        ])
        return dumps(postsList)
