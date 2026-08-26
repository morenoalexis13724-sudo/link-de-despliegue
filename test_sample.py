import pytest
from sample_app import sample_app

@pytest.fixture
def client():
    sample_app.config["TESTING"] = True
    with sample_app.test_client() as client:
        yield client


def test_pagina_principal(client):
    response = client.get("/")

    if response.status_code != 200:
        raise AssertionError(
            f"Se esperaba código 200, pero se obtuvo {response.status_code}"
        )
    
    


