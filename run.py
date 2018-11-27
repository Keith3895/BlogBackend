from flask import Flask, Blueprint
from flask_restful import Resource,Api

from blogREST.resources.post.controllers import postInfo
from blogREST.common.utils import get_instance_folder_path
from blogREST.config import configure_app

app = Flask(__name__, instance_path=get_instance_folder_path(),
            instance_relative_config=True)

configure_app(app)
api = Api(app)


api.add_resource(postInfo,'/postInfo')

if __name__ == '__main__':
    app.run() 