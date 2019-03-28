from flask import Flask,Blueprint
from flask_restplus import Api
import jwt
from blogREST.common.Exception import ValidationException

# User defined resource controllers.
from .user.controllers import api as ns1
from .auth.controllers import api as ns2
from .post.controllers import api as ns3 

blueprint = Blueprint('api', __name__, url_prefix='/api')

api = Api(blueprint,
    title='Blog Backend Apis',
    description='List of all the Api that can be consumed by any client system.'
)


@api.errorhandler(ValidationException)
def handle_validation_exception(error):
    return {'message': 'Validation error', 'errors': {error.error_field_name: error.message}}, 400

@api.errorhandler(jwt.ExpiredSignatureError)
def handle_expired_signature_error(error):
    return {'message': 'Token expired'}, 401


@api.errorhandler(jwt.InvalidTokenError)
@api.errorhandler(jwt.DecodeError)
@api.errorhandler(jwt.InvalidIssuerError)
def handle_invalid_token_error(error):
    return {'message': 'Token incorrect, supplied or malformed'}, 401


api.add_namespace(ns1)
api.add_namespace(ns2)
api.add_namespace(ns3)
