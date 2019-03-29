import pytest
from blogREST import server
print('test')
# Creates a fixture whose name is "app"
# and returns our flask server instance
@pytest.fixture
def app():
    app = server.app
    return app