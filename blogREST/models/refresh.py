import os
from pymodm import MongoModel, fields
from pymodm.connection import connect

from dotenv import load_dotenv
load_dotenv()

connect(os.getenv('mongourl'), alias="blog-api")

class RefreshToken(MongoModel):
    user_id = fields.CharField(required=True)
    refresh_token = fields.CharField(required=True)
    user_agent_hash = fields.CharField(required=True)
    

    class Meta:
        connection_alias = 'blog-api'
