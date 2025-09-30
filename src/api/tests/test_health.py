from fastapi.testclient import TestClient
import pytest
from main import app
import os

# Set up environment (can be refactored into conftest.py if reused often)
os.environ["SQLITE_DB_PATH"] = "/Users/samanthamarriott/Documents/hotspot/src/data/hotspot.db"

client = TestClient(app)


def test_health_success():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.text.strip('"') == "ok"  # keep the quotes stripped
    
def test_health_wrong_path():
    """Incorrect path should return 404"""
    response = client.get("/api/v1/healthz")
    assert response.status_code == 404


@pytest.mark.parametrize("method", ["post", "put", "delete", "patch"])
def test_health_invalid_methods(method):
    response = getattr(client, method)("/api/health")  # ✅ correct path
    assert response.status_code == 405


def test_health_response_format():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert isinstance(response.text, str)
    assert response.text.strip('"') == "ok"

