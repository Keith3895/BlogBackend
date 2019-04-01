from flask_restplus import fields

contentPost = {
    '_id': fields.String,
    'slug':fields.String,
    'title':fields.String,
    'user_id':fields.String,
    'content':fields.String
}


post_contentPost = {
    'slug':fields.String,
    'title':fields.String,
    'user_id':fields.String,
    'content':fields.String
}

def get_post_model(req_type='GET'):
    if req_type == 'POST':
        return post_contentPost
    return contentPost