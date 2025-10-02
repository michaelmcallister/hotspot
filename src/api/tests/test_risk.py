import requests

BASE_URL = "http://localhost:8000"

def test_risk_top_default():
    """Test default risk ranking (suburbs)"""
    response = requests.get(f"{BASE_URL}/api/v1/risk/top")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    for item in data["items"]:
        assert "suburb" in item
        assert "postcode" in item
        assert "risk_score" in item
        assert 0 <= item["risk_score"] <= 1

def test_risk_top_scope_lga():
    """Test risk ranking grouped by LGA"""
    params = {"scope": "lga"}
    response = requests.get(f"{BASE_URL}/api/v1/risk/top", params=params)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    for item in data["items"]:
        assert "lga" in item
        assert "avg_risk" in item
        assert 0 <= item["avg_risk"] <= 1
        assert "postcode_count" in item

def test_risk_top_pagination():
    """Test pagination parameters"""
    params = {"page": 1, "itemsPerPage": 5}
    response = requests.get(f"{BASE_URL}/api/v1/risk/top", params=params)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) <= 5
    assert "total" in data

def test_risk_top_sorting():
    """Test sortBy and sortOrder parameters"""
    params = {"sortBy": "risk_score", "sortOrder": "desc"}
    response = requests.get(f"{BASE_URL}/api/v1/risk/top", params=params)
    assert response.status_code == 200
    data = response.json()
    risk_scores = [item.get("risk_score", item.get("avg_risk")) for item in data["items"]]
    assert risk_scores == sorted(risk_scores, reverse=True)

def test_risk_top_search_filter():
    """Test search filter for suburb"""
    params = {"search": "Richmond"}
    response = requests.get(f"{BASE_URL}/api/v1/risk/top", params=params)
    assert response.status_code == 200
    data = response.json()
    for item in data["items"]:
        if "suburb" in item:
            assert "richmond" in item["suburb"].lower()

def test_risk_top_search_filter_empty():
    """Searching for a nonexistent suburb returns empty items list"""
    params = {"search": "NotASuburb"}
    response = requests.get(f"{BASE_URL}/api/v1/risk/top", params=params)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 0

def test_risk_top_invalid_params():
    """Test invalid query parameters return 422 or default to normal behavior"""
    params = {"scope": "invalid_scope", "page": -1, "itemsPerPage": -5}
    response = requests.get(f"{BASE_URL}/api/v1/risk/top", params=params)
    # Either validation error (422) or fallback/default response (200)
    assert response.status_code in (200, 422)

