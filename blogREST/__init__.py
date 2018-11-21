from flask import Flask
from blogREST.post.controllers import post
from blogREST.utils import get_instance_folder_path
from blogREST.config import configure_app

app = Flask(__name__, instance_path=get_instance_folder_path(),
            instance_relative_config=True)
configure_app(app)

app.register_blueprint(post, url_prefix='/post')
