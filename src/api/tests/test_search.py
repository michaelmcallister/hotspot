from fastapi.testclient import TestClient
from main import app
import os
os.environ["SQLITE_DB_PATH"] = "/Users/samanthamarriott/Documents/hotspot/src/data/hotspot.db"

client = TestClient(app)

def test_search_basic():
    response = client.get("/api/v1/search?q=Richmond")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:  # only check keys if data exists
        assert "suburb" in data[0]
        assert "risk_score" in data[0]

def test_search_empty_query():
    response = client.get("/api/v1/search?q=")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    if data:
        assert "label" in data[0]
        assert "postcode" in data[0]
        assert "risk_score" in data[0]

def test_search_multiple_valid_queries():
    queries = ["Richmond", "Fitzroy", "Abbotsford", "Melbourne"]
    for q in queries:
        response = client.get(f"/api/v1/search?q={q}")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        if data:
            assert "suburb" in data[0]
            assert "risk_score" in data[0]
            
def test_search_case_insensitive():
    response_lower = client.get("/api/v1/search?q=richmond")
    response_upper = client.get("/api/v1/search?q=RICHMOND")
    response_mixed = client.get("/api/v1/search?q=RiChMoNd")

    assert response_lower.status_code == 200
    assert response_upper.status_code == 200
    assert response_mixed.status_code == 200

    # Compare results are identical
    assert response_lower.json() == response_upper.json() == response_mixed.json()

def test_search_partial_match():
    response = client.get("/api/v1/search?q=Rich")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert any("richmond" in d["label"].lower() for d in data)

def test_search_nonexistent():
    response = client.get("/api/v1/search?q=THISDOESNOTEXIST")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0  # Should return empty list

def test_search_limit():
    response = client.get("/api/v1/search?q=Richmond")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_search_special_characters():
    response = client.get("/api/v1/search?q=St Kilda")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert any("st kilda" in d["label"].lower() for d in data)

def test_search_response_schema():
    response = client.get("/api/v1/search?q=Melbourne")
    data = response.json()
    required_keys = {"label", "suburb", "postcode", "risk_score"}
    for item in data:
        assert required_keys.issubset(item.keys())










