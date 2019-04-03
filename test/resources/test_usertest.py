import os
import json
import pytest
# client is a fixture, injected by the `pytest-flask` plugin

data = {
    "username": "TestAccount25",
    "email": "TestAccount@asd.com",
    "password": "1234facW",
    "first_name": "test",
    "last_name": "string",
    "dob": "2019-03-26T13:02:22.190Z"
}


@pytest.mark.run(order=1)
def test_register(client):
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    url = '/api/user/register'

    response = client.post(url, data=json.dumps(data), headers=headers)
    print(response.json)
    assert response.content_type == mimetype
    assert isinstance(response.json['username'], str)
    assert data['password'] != response.json['password']


@pytest.mark.run(order=2)
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


@pytest.mark.run(order=3)
def test_login(client):

    data2 = {
        "username": "TestAccount25",
        "password": "1234facW"
    }
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    url = '/api/auth/jwt/login'
    response = client.post(url, data=json.dumps(data2), headers=headers)
    assert 'access_token' in response.json


@pytest.mark.run(after='test_login')
def test_addPost(client):
    access_token = getAccess(client)
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype,
        'Authorization': "Bearer "+access_token
    }
    url = '/api/post/blog'
    for x in range(10):
        blog = {
            "title": "string test for post {}".format(x),
            "content": "Lorem ipsum, dolor sit amet consectetur adipisicing elit. Maiores magni eveniet porro, laudantium nulla vitae. Hic numquam est veniam quasi consectetur reprehenderit. Sapiente deleniti optio sit minus reiciendis distinctio tempora."
        }
        response = client.post(url, data=json.dumps(blog), headers=headers)
        assert 'slug' in response.json
        assert "title" in response.json
        assert "content" in response.json
        assert "CreatDate" in response.json
        assert "author" in response.json


def getAccess(client):
    data2 = {
        "username": "TestAccount25",
        "password": "1234facW"
    }
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }

    url = '/api/auth/jwt/login'

    response = client.post(url, data=json.dumps(data2), headers=headers)
    return response.json['access_token']


@pytest.mark.run(after='test_addPost')
def test_mongoClear(client):
    from pymongo import MongoClient
    connectionString = os.getenv('mongourl')
    client = MongoClient(connectionString)
    db = connectionString.split('/')[3]
    if db:
        client.drop_database(db)
        print('clearing Database')
        assert True
