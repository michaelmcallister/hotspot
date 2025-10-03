import requests

BASE_URL = "http://localhost:8000"

def test_feed_valid_postcode():
    postcode = "3737"
    response = requests.get(f"{BASE_URL}/api/v1/postcode/{postcode}/feed")
    assert response.status_code == 200

    data = response.json()
    assert "current" in data
    assert "nearest_safer_suburbs" in data
    assert "parking_submissions" in data

    assert data["current"]["postcode"] == postcode
    assert "risk_score" in data["current"]
    assert "suburb" in data["current"]

    assert isinstance(data["parking_submissions"], list)


def test_feed_nonexistent_postcode():
    postcode = "9999"
    response = requests.get(f"{BASE_URL}/api/v1/postcode/{postcode}/feed")
    assert response.status_code == 200

    data = response.json()
    assert "current" in data
    assert "nearest_safer_suburbs" in data
    assert "parking_submissions" in data
    assert data["current"]["postcode"] == postcode
    assert isinstance(data["parking_submissions"], list)
    assert len(data["parking_submissions"]) == 0


def test_feed_invalid_postcode_format():
    """Postcode with invalid format (non-numeric) should return 422"""
    postcode = "ABCD"
    response = requests.get(f"{BASE_URL}/api/v1/postcode/{postcode}/feed")
    assert response.status_code == 422


def test_feed_empty_postcode():
    response = requests.get(f"{BASE_URL}/api/v1/postcode//feed")
    assert response.status_code == 200
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Not found"

def test_feed_missing_postcode():
    response = requests.get(f"{BASE_URL}/api/v1/postcode/feed")
    assert response.status_code == 200
    data = response.json()
    assert "detail" in data
    assert data["detail"] == "Not found"

def test_feed_postcode_with_spaces():
    postcode = " 3737 "
    response = requests.get(f"{BASE_URL}/api/v1/postcode/{postcode.strip()}/feed")
    assert response.status_code == 200
    data = response.json()
    assert "current" in data
    assert data["current"]["postcode"] == postcode.strip()


def test_feed_postcode_numeric_edge_cases():
    for postcode in ["0000", "9999"]:
        response = requests.get(f"{BASE_URL}/api/v1/postcode/{postcode}/feed")
        if postcode == "0000":
            assert response.status_code in (404, 422)
        else:
            assert response.status_code == 200
            data = response.json()
            assert "parking_submissions" in data



