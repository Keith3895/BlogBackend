## USER MODELS TO MARSHAL WITH ##

from flask_restplus import fields

user_model_non_admin = {
    '_id': fields.String,
    'email': fields.String,
    'first_name': fields.String,
    'last_name': fields.String
}

user_model_for_admin = {
    '_id': fields.String,
    'email': fields.String,
    'password': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'dob': fields.Date
}

return_token_model =  {
    'access_token': fields.String(required=True),
    'refresh_token': fields.String(required=True)
}

post_user_model = {
    'username': fields.String(required=True, description="User Name"),
    'email': fields.String(required=True, description="Email address"),
    'password': fields.String(required=True, description="Password"),
    'first_name': fields.String(required=True, description="First name"),
    'last_name': fields.String(required=True, description="Last Name"),
    'dob': fields.Date(description="Date format (ISO 8601): yyyy-mm-dd")
}

def get_user_model(req_type='GET'):
    if req_type == 'POST':
        return post_user_model
    return user_model_non_admin