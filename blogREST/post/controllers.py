from flask import Blueprint


post = Blueprint('post', __name__)


@post.route('/')
def index():
    return "Main"