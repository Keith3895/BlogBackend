from flask_restplus import fields

contentPost = {
    'slug': fields.String,
    'title': fields.String,
    'user_id': fields.String,
    'content': fields.String,
    'CreatDate': fields.Date,
    'author': fields.String,
    'tags': fields.List(fields.String)
}


post_contentPost = {
    'title': fields.String,
    'slug': fields.String,
    'content': fields.String,
    'CreatDate': fields.Date,
    'tags': fields.List(fields.String)
}


def get_post_model(req_type='GET'):
    if req_type == 'POST':
        return post_contentPost
    return contentPost