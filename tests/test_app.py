import pytest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
from app import app as flask_app

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"

def test_get_assets(client):
    res = client.get("/assets")
    assert res.status_code == 200
    assert "assets" in res.get_json()

def test_get_asset_not_found(client):
    res = client.get("/assets/999")
    assert res.status_code == 404

def test_create_asset(client):
    res = client.post("/assets", json={"name": "Switch-003"})
    assert res.status_code == 201
    assert res.get_json()["name"] == "Switch-003"

def test_create_asset_missing_name(client):
    res = client.post("/assets", json={})
    assert res.status_code == 400
