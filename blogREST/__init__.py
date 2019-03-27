import jwt
from flask import Flask
from flask_restplus import Resource,Api
from blogREST.resources.user.controllers import user_blueprint
from blogREST.resources.auth.controllers import auth_blueprint
from blogREST.resources.post.controllers import postInfo_blueprint  
from blogREST.common.utils import get_instance_folder_path
from blogREST.config import configure_app
from blogREST.common.Exception import ValidationException
# from pymodm import connect

app = Flask(__name__, instance_path=get_instance_folder_path(),
            instance_relative_config=True)

app.secret_key = "Blog API secret key for sessions"

app.register_blueprint(auth_blueprint, url_prefix='/api')
app.register_blueprint(user_blueprint, url_prefix='/api/user')
app.register_blueprint(postInfo_blueprint, url_prefix='/api/post')


