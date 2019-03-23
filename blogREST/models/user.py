import os
from pymodm import MongoModel, fields
from pymodm.connection import connect

from dotenv import load_dotenv
load_dotenv()

connect(os.getenv('mongourl'), alias="blog-api")

class User(MongoModel):
    email = fields.EmailField(required=True)
    password = fields.CharField(required=True)
    first_name = fields.CharField(required=True)
    last_name = fields.CharField(required=True)
    dob = fields.DateTimeField()

    class Meta:
        connection_alias = 'blog-api'
