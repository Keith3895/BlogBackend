from blogREST.resources.user import *
import json

# client is a fixture, injected by the `pytest-flask` plugin

data = {
    "username": "TestAccount4",
    "email": "TestAccount@asd.com",
    "password": "1234facW",
    "first_name": "test",
    "last_name": "string",
    "dob": "2019-03-26T13:02:22.190Z"
}

def test_register(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    url = '/api/user/register'

    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.content_type == mimetype
    assert isinstance(response.json['username'], str)
    assert data['password'] != response.json['password']

def test_registerNegative(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    url = '/api/user/register'

    response = client.post(url, data=json.dumps(data), headers=headers)
    assert response.content_type == mimetype
    assert 'errors' in response.json
