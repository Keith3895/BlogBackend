import os
from pymodm import MongoModel, fields
from pymodm.connection import connect

connect(os.getenv('mongourl'), alias="blog-api")

class Post(MongoModel):
    slug = fields.CharField(required=True)
    title = fields.CharField(required=True)
    user_id = fields.CharField(required=True)
    content = fields.CharField(required=True)
    CreatDate = fields.DateTimeField(required=True)
    tags = fields.ListField(fields.CharField())
    author = fields.CharField(required=True)