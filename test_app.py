import pytest
from app import app  # assuming your Flask app is in app.py


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_index(client):
    """Test if the index page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Latent Semantic Analysis (LSA) Search Engine" in response.data


def test_search(client):
    """Test if the search functionality works."""
    response = client.post('/search', data={'query': 'test'})
    assert response.status_code == 200

    json_data = response.get_json()
    assert 'documents' in json_data
    assert 'similarities' in json_data
    assert 'indices' in json_data
    assert len(json_data['documents']) > 0
