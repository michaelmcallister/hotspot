from fastapi.testclient import TestClient
from main import app
import os
import pytest

os.environ["SQLITE_DB_PATH"] = "/Users/samanthamarriott/Documents/hotspot/src/data/hotspot.db"

client = TestClient(app)

def test_risk_compare_success():
    response = client.get("/api/v1/risk/compare?postcode=3067")
    assert response.status_code == 200
    data = response.json()
    assert "base" in data
    assert "defaults" in data
    assert "postcode" in data["base"]
    assert "risk_score" in data["base"]

def test_risk_compare_missing_params():
    response = client.get("/api/v1/risk/compare")
    assert response.status_code == 422

def test_risk_compare_invalid_postcodes():
    response = client.get("/api/v1/risk/compare?postcode1=abcd&postcode2=1234")
    assert response.status_code == 422

@pytest.mark.parametrize("method", ["post", "put", "delete", "patch"])
def test_risk_compare_invalid_methods(method):
    response = getattr(client, method)("/api/v1/risk/compare?postcode1=3067&postcode2=3737")
    assert response.status_code == 405

@pytest.mark.parametrize("pc", ["3067", "3737", "3000"])
def test_risk_compare_multiple_valid_postcodes(pc):
    response = client.get(f"/api/v1/risk/compare?postcode={pc}")
    assert response.status_code == 200
    data = response.json()
    assert data["base"]["postcode"] == pc

def test_risk_compare_field_types():
    response = client.get("/api/v1/risk/compare?postcode=3067")
    data = response.json()
    base = data["base"]
    assert isinstance(base["postcode"], str)
    assert isinstance(base["risk_score"], (int, float))

def test_risk_compare_defaults_empty():
    response = client.get("/api/v1/risk/compare?postcode=3067")
    data = response.json()
    assert "defaults" in data

def test_risk_compare_risk_score_range():
    response = client.get("/api/v1/risk/compare?postcode=3067")
    base = response.json()["base"]
    assert 0 <= base["risk_score"] <= 100

def test_risk_compare_defaults_keys():
    response = client.get("/api/v1/risk/compare?postcode=3067")
    data = response.json()
    if data["defaults"]:
        expected_keys = ["model_default_risk", "postcode_default_risk"]
        for key in expected_keys:
            assert key in data["defaults"]
            
def test_risk_compare_nonexistent_postcode():
    """Non-existent postcode returns base as empty or defaults"""
    response = client.get("/api/v1/risk/compare?postcode=9999")
    assert response.status_code == 200
    data = response.json()
    assert "base" in data
    # base might be None or empty dict depending on DB

def test_risk_compare_response_time():
    """Response should be reasonably fast"""
    response = client.get("/api/v1/risk/compare?postcode=3067")
    assert response.status_code == 200
    # Example: ensure request completes under 1 second
    assert response.elapsed.total_seconds() < 1





