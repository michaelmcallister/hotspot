import requests

BASE_URL = "http://localhost:8000"

def test_risk_top_default():
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
    params = {"page": 1, "itemsPerPage": 5}
    response = requests.get(f"{BASE_URL}/api/v1/risk/top", params=params)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) <= 5
    assert "total" in data

def test_risk_top_sorting():
    params = {"sortBy": "risk_score", "sortOrder": "desc"}
    response = requests.get(f"{BASE_URL}/api/v1/risk/top", params=params)
    assert response.status_code == 200
    data = response.json()
    risk_scores = [item.get("risk_score", item.get("avg_risk")) for item in data["items"]]
    assert risk_scores == sorted(risk_scores, reverse=True)

def test_risk_top_search_filter():
    params = {"search": "Richmond"}
    response = requests.get(f"{BASE_URL}/api/v1/risk/top", params=params)
    assert response.status_code == 200
    data = response.json()
    for item in data["items"]:
        if "suburb" in item:
            assert "richmond" in item["suburb"].lower()

def test_risk_top_search_filter_empty():
    params = {"search": "NotASuburb"}
    response = requests.get(f"{BASE_URL}/api/v1/risk/top", params=params)
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) == 0

def test_risk_top_invalid_params():
    params = {"scope": "invalid_scope", "page": -1, "itemsPerPage": -5}
    response = requests.get(f"{BASE_URL}/api/v1/risk/top", params=params)
    assert response.status_code in (200, 422)

