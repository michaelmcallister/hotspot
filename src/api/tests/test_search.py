import requests

BASE_URL = "http://localhost:8000"

def test_search_by_suburb():
    response = requests.get(f"{BASE_URL}/api/v1/search", params={"q": "Richmond"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any("richmond" in item["label"].lower() for item in data)


def test_search_by_suburb_case_insensitive():
    queries = ["richmond", "RICHMOND", "RiChMoNd"]
    results = []
    for q in queries:
        response = requests.get(f"{BASE_URL}/api/v1/search", params={"q": q})
        assert response.status_code == 200
        data = response.json()
        results.append({item["label"] for item in data})
    assert all(r == results[0] for r in results[1:])


def test_search_partial_match():
    response = requests.get(f"{BASE_URL}/api/v1/search", params={"q": "Rich"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        assert "rich" in item["label"].lower()


def test_search_by_postcode():
    response = requests.get(f"{BASE_URL}/api/v1/search", params={"q": "3000"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(item["postcode"] == "3000" for item in data)


def test_search_empty_query():
    response = requests.get(f"{BASE_URL}/api/v1/search", params={"q": ""})
    assert response.status_code == 422


def test_search_invalid_query():
    response = requests.get(f"{BASE_URL}/api/v1/search", params={"q": ""})
    assert response.status_code == 422


def test_search_nonexistent_suburb():
    response = requests.get(f"{BASE_URL}/api/v1/search", params={"q": "NotASuburb"})
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_search_risk_score_range():
    response = requests.get(f"{BASE_URL}/api/v1/search", params={"q": "Richmond"})
    data = response.json()
    for item in data:
        assert 0 <= item["risk_score"] <= 1


def test_search_edge_cases():
    invalid_queries = ["@#$", "!!!", "123abc!"]
    for q in invalid_queries:
        response = requests.get(f"{BASE_URL}/api/v1/search", params={"q": q})
        assert response.status_code in (200, 422)


def test_search_sorting():
    params = {"q": "Richmond", "sortBy": "risk_score", "sortOrder": "desc"}
    response = requests.get(f"{BASE_URL}/api/v1/search", params=params)
    assert response.status_code == 200
    data = response.json()
    risk_scores = [item["risk_score"] for item in data]
    assert risk_scores == sorted(risk_scores, reverse=True)


def test_search_lga_consistency():
    expected_lga = {
        "RICHMOND": "Yarra",
        "MELBOURNE": "Melbourne",
    }
    response = requests.get(f"{BASE_URL}/api/v1/search", params={"q": "RICHMOND"})
    assert response.status_code == 200
    data = response.json()
    for item in data:
        suburb = item["suburb"]
        expected = expected_lga.get(suburb)
        if expected:
            assert item["lga"].strip().lower() == expected.strip().lower()
