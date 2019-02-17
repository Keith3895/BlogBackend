####### STANDARD/INSTALLED PACKAGES #######
from flask import Flask, Blueprint, jsonify, redirect, url_for, session
from flask_restplus import Resource, Api, fields
from flask_pymongo import PyMongo
from flask_dance.contrib.google import make_google_blueprint, google

####### USER DEFINED PACKAGES #######
from blogREST.models.user import User
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


api = Api(auth_blueprint)

@api.route('/login')
class googleLogin(Resource):
    def get(self):
        if not google.authorized:
            return redirect(url_for("google.login"))
        resp = google.get("/oauth2/v2/userinfo")
        assert resp.ok, resp.text
        session['user_id'] = resp.json()["email"]
        # return "You are {email} on Google".format(email=resp.json()["email"])
        return resp.json()


@api.route('/logout')
class googleLogout(Resource):
    def get(self):
        if not google.authorized:
            return {'message': 'You are not logged in! To login go to /api/login'}
        token = auth_blueprint.token["access_token"] 
        email = session["user_id"]
        resp = google.post('https://accounts.google.com/o/oauth2/revoke',
            params={'token': token},
            headers = {'content-type': 'application/x-www-form-urlencoded'}
        )
        if resp.ok:
            session.clear()
            # logout_user()
            message = f'User {email} is successfully logged out'
            return {'message': message}

        
    