from pymodm import MongoModel, fields

class User(MongoModel):
    email = fields.EmailField()
    password = fields.CharField(required=True)

    class Meta:
        connection_alias = 'test'
