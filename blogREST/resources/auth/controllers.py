####### STANDARD/INSTALLED PACKAGES #######
from flask import current_app, request, Flask, Blueprint, jsonify, redirect, url_for, session
from flask_restplus import Resource, Api, fields
from flask_pymongo import PyMongo
from flask_dance.contrib.google import make_google_blueprint, google
import re
import jwt
import datetime
import hashlib
import bson
from bson.json_util import dumps

####### USER DEFINED PACKAGES #######
from blogREST.models.user import User
from blogREST.models.refresh import RefreshToken
from blogREST.models.api_model.user import get_user_model
from blogREST.common.utils import get_mongo_collection


auth_blueprint = make_google_blueprint(
    client_id="176380596073-606s9n77bkf98gj5pu09fc4v7bujb4ii.apps.googleusercontent.com",
    client_secret="w2WH9F4VkuknETVMBwOvzAWn",
    scope=[
        "https://www.googleapis.com/auth/plus.me",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile"
    ]
)
userCollection = get_mongo_collection('User')
refreshTokenCollection = get_mongo_collection('RefreshToken')
api = Api(auth_blueprint)


'''
API Models
'''

loginModel = api.model('Login', {
    'username': fields.String(required=True),
    'password': fields.String(required=True)
})

return_token_model = api.model('ReturnToken', {
    'access_token': fields.String(required=True),
    'refresh_token': fields.String(required=True)
})

'''
End of API Models
'''


@api.errorhandler(jwt.ExpiredSignatureError)
def handle_expired_signature_error(error):
    return {'message': 'Token expired'}, 401


@api.errorhandler(jwt.InvalidTokenError)
@api.errorhandler(jwt.DecodeError)
@api.errorhandler(jwt.InvalidIssuerError)
def handle_invalid_token_error(error):
    return {'message': 'Token incorrect, supplied or malformed'}, 401


@api.route('/oauth/login')
class googleLogin(Resource):
    def get(self):
        if not google.authorized:
            return redirect(url_for("google.login"))
        resp = google.get("/oauth2/v2/userinfo")
        assert resp.ok, resp.text
        session['user_id'] = resp.json()["email"]
        # return "You are {email} on Google".format(email=resp.json()["email"])
        return resp.json()


@api.route('/oauth/logout')
class googleLogout(Resource):
    def get(self):
        if not google.authorized:
            return {'message': 'You are not logged in! To login go to /api/login'}
        token = auth_blueprint.token["access_token"]
        email = session["user_id"]
        resp = google.post('https://accounts.google.com/o/oauth2/revoke',
                           params={'token': token},
                           headers={
                               'content-type': 'application/x-www-form-urlencoded'}
                           )
        if resp.ok:
            session.clear()
            # logout_user()
            message = f'User {email} is successfully logged out'
            return {'message': message}


@api.route('/jwt/login')
class Log(Resource):
    '''
    the following method is called to generate a bson object to insert into 
    Refresh Token Collection. 
    '''

    def refresTokenGenerator(self, user_id, refresh_token, user_agent_hash):
        import collections  # From Python standard library.
        import bson
        from bson.codec_options import CodecOptions
        # refreshTokenJSON =
        data = bson.BSON.encode({
            "user_id": user_id,
            "refresh_token": refresh_token,
            "user_agent_hash": user_agent_hash
        })
        decoded_doc = bson.BSON.decode(data)
        options = CodecOptions(document_class=collections.OrderedDict)
        decoded_doc = bson.BSON.decode(data, codec_options=options)

        return decoded_doc

    @api.expect(loginModel)
    @api.response(200, 'Success', return_token_model)
    @api.response(401, 'Incorrect username or password')
    def post(self):
        """
        This API implemented JWT. Token's payload contain:
        'uid' (user id),
        'exp' (expiration date of the token),
        'iat' (the time the token is generated)
        """
        user = userCollection.find_one({"username": api.payload['username']})
        if not user:
            api.abort(401, 'Incorrect username or password')
        from blogREST.common.utils import check_password
        if check_password(user['password'], api.payload['password']):
            _access_token = jwt.encode({'uid': user['uid'],
                                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
                                        'iat': datetime.datetime.utcnow()},
                                       current_app.config['SECRET_KEY']).decode('utf-8')
            _refresh_token = jwt.encode({'uid': user['uid'],
                                         'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                                         'iat': datetime.datetime.utcnow()},
                                        current_app.config['SECRET_KEY']).decode('utf-8')

            user_agent_string = request.user_agent.string.encode('utf-8')
            user_agent_hash = hashlib.md5(user_agent_string).hexdigest()

            refresh_token = refreshTokenCollection.find(
                {"user_agent_hash": user_agent_hash})
            print(list(refresh_token))
            if not len(list(refresh_token)):
                refresh_token = self.refresTokenGenerator(user_id=user['uid'], refresh_token=_refresh_token,
                                                          user_agent_hash=user_agent_hash)
                refreshTokenCollection.insert_one(refresh_token)
            else:
                refresh_token.refresh_token = _refresh_token
                refreshTokenCollection.update(
                    {"user_agent_hash": user_agent_hash}, refresh_token, upsert=True)

            return {'access_token': _access_token, 'refresh_token': _refresh_token}, 200

        api.abort(401, 'Incorrect username or password')


@api.route('/jwt/refresh')
class Refresh(Resource):
    @api.expect(api.model('RefreshToken', {'refresh_token': fields.String(required=True)}), validate=True)
    @api.response(200, 'Success', return_token_model)
    def post(self):
        _refresh_token = api.payload['refresh_token']
        try:
            payload = jwt.decode(
                _refresh_token, current_app.config['SECRET_KEY'])
            refresh_token = refreshTokenCollection.find_one(
                {"user_id": payload['uid'], "refresh_token": _refresh_token})

            if not len(list(refresh_token)):
                raise jwt.InvalidIssuerError

            # Generate new pair
            _access_token = jwt.encode({'uid': refresh_token['user_id'],
                                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15),
                                        'iat': datetime.datetime.utcnow()},
                                       current_app.config['SECRET_KEY']).decode('utf-8')
            _refresh_token = jwt.encode({'uid': refresh_token['user_id'],
                                         'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                                         'iat': datetime.datetime.utcnow()},
                                        current_app.config['SECRET_KEY']).decode('utf-8')
            
            refresh_token['refresh_token'] = _refresh_token
            refreshTokenCollection.update(
                {"user_id": payload['uid'], "refresh_token": _refresh_token}, refresh_token)

            return {'access_token': _access_token, 'refresh_token': _refresh_token}, 200

        except jwt.ExpiredSignatureError as e:
            raise e
        except (jwt.DecodeError, jwt.InvalidTokenError)as e:
            raise e
        except:
            # print(e)
            api.abort(401, 'Unknown token error')
