import pytest
from blogREST import server
import os
from pymongo import MongoClient
# Creates a fixture whose name is "app"
# and returns our flask server instance


connectionString = os.getenv('mongourl')
client = MongoClient(connectionString)
db = connectionString.split('/')[3]
if db:
    client.drop_database(db)


@pytest.fixture
def app():
    app = server.app
    return app
