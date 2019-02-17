from pymodm import MongoModel, fields
from pymodm.connection import connect

connect("mongodb://keimo:keimo123@ds141924.mlab.com:41924/blog-db", alias="blog-api")

class User(MongoModel):
    email = fields.EmailField(required=True)
    password = fields.CharField(required=True)
    first_name = fields.CharField(required=True)
    last_name = fields.CharField(required=True)
    dob = fields.DateTimeField()

    class Meta:
        connection_alias = 'blog-api'
