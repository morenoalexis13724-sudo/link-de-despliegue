import pytest
from sample_app import sample_app

@pytest.fixture
def client():
    sample_app.config["TESTING"] = True
    with sample_app.test_client() as client:
        yield client


def test_pagina_principal(client):
    response = client.get("/")
    assert response.status_code == 200
    


