import pytest
import sys
import os
path = os.getcwd()
sys.path.append(path+"/src/")
from backend import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    # other setup can go here
    yield app

@pytest.fixture()
def client(app):
    return app.test_client()


# Check connection to index page
def test_index_connection(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'jikAPI' in response.data

# Check connection to api-docs page
def test_api_page(client):
    response = client.get('/api/v2/')
    assert response.status_code == 200
    assert b'Flasgger' in response.data

# Check connection to unsubscribe page
def test_unsubscribepage_connection(client):
    response = client.get('/api/v2/newsletter/unsubscribe')
    assert response.status_code == 200
    assert b'Unsubscribe' in response.data

if __name__ == '__main__':
    pytest.main()
