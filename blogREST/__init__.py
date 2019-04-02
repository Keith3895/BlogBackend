# import jwt
from flask import Flask,Blueprint
from flask_restplus import Resource,Api

from blogREST.config import configure_app
from blogREST.common.utils import get_instance_folder_path

class Server():
    def __init__(self):
        self.app = Flask(__name__, instance_path=get_instance_folder_path(),
            instance_relative_config=True)
        configure_app(self.app)
        from blogREST.resources import blueprint as blueprint1
        self.app.register_blueprint(blueprint1)
    def run(self):
        self.app.run()

server = Server()