from flask import Flask, Blueprint, jsonify, redirect, url_for, session
from flask_restplus import Resource, Api, fields, Namespace, reqparse
from flask_pymongo import PyMongo
from bson.json_util import dumps

from blogREST.resources.auth.controllers import token_required

from blogREST.models.post import Post
from blogREST.common.utils import get_mongo_collection
from blogREST.models.api_model.post import get_post_model


'''
project and limit is used for the aggrigate query that is used 
to fetch the response from the database.
'''

project = {
    "$project":
        {
            "slug": 1,
            "title": 1,
            "author": 1,
            "CreatDate": 1,
            "tags": 1,
            "content": {"$substr": ["$content", 0, 20]}
        }
}
limit = 10


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
postResModel = api.model('Add New Blog Post', get_post_model('GET'))


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
    @api.expect(postResModel)
    @api.header('application/json')
    @api.doc(security='apikey')
    @token_required
    def post(self, current_user):
        import uuid
        import datetime

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
@api.doc(params={
    'date': 'the date filter to retrive blog posts.',
    'pageNumber': 'The page number to be retrieved.',
    'fromDate': 'the from date value for range filter.',
    'toDate': 'the End date value for range filter.'
})
class ListByDate(Resource):

    project = {
        "$project":
        {
            "slug": 1,
            "title": 1,
            "author": 1,
            "CreatDate": 1,
            "content": {"$substr": ["$content", 0, 20]},
            "tags": 1,
        }
    }
    limit = 10

    @api.header('application/json')
    @api.marshal_with(postResModel)
    def get(self, date=None, fromDate=None, toDate=None, pageNumber=1):
        if isinstance(pageNumber, str):
            pageNumber = int(pageNumber, 2)
        import datetime
        if date:
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
            match = {
                "$match": {
                    "CreatDate": {
                        "$gte": date,
                        "$lt": (date+datetime.timedelta(days=1))
                    }
                }
            }
        else:
            fromDate = datetime.datetime.strptime(fromDate, '%Y-%m-%d')
            toDate = datetime.datetime.strptime(toDate, '%Y-%m-%d')
            match = {
                "$match": {
                    "CreatDate": {
                        "$gte": fromDate,
                        "$lt": toDate,
                    }
                }
            }

        skips = limit * (pageNumber - 1)
        postsList = postCollection.aggregate([
            match,
            project,
            {"$skip": skips},
            {"$limit": limit},
            {"$sort": {'CreatDate': -1}}
        ])
        return dumps(postsList)


@api.doc(params={
    'pageNumber': 'The page number to be retrieved.'
})
@api.marshal_with(postResModel)
@api.route('/list/<pageNumber>')
class GeneralList(Resource):
    def get(self, pageNumber=1):
        if isinstance(pageNumber, str):
            pageNumber = int(pageNumber, 2)
        skips = limit * (pageNumber - 1)
        postsList = postCollection.aggregate([
            project,
            {"$skip": skips},
            {"$limit": limit},
            {"$sort": {'CreatDate': -1}}
        ])
        return dumps(postsList)

    @api.expect(api.model('test', {
        "tags": fields.List(fields.String)
    }))
    @api.header('application/json')
    def post(self, pageNumber=1):
        '''
        Api returns list of blog posts with pagesize = 10.
        '''
        if isinstance(pageNumber, str):
            pageNumber = int(pageNumber, 2)
        tags = api.payload['tags']
        match = {
            "$match": {
                "tags": {
                    "$in": tags
                }
            }
        }

        skips = limit * (pageNumber - 1)
        postsList = postCollection.aggregate([
            match,
            project,
            {"$skip": skips},
            {"$limit": limit},
            {"$sort": {'CreatDate': -1}}
        ])
        return dumps(postsList)
