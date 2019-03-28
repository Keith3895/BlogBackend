import os
from pymodm import MongoModel, fields
from pymodm.connection import connect
from dotenv import load_dotenv


load_dotenv()
connect(os.getenv('mongourl'), alias="blog-api")

class Post(MongoModel):
    slug = fields.CharField(required=True)
    title = fields.CharField(required=True)
    user_id = fields.CharField(required=True)
    content = fields.CharField(required=True)
