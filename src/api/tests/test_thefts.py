# tests/test_thefts.py
import requests
import os

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")


def test_thefts_valid_postcode():
    postcode = "3737"
    response = requests.get(f"{BASE_URL}/api/v1/postcode/{postcode}/thefts")
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    if data:  # only check structure if list not empty
        assert "year" in data[0]
        assert "thefts" in data[0]  # API uses "thefts" not "theft_count"
        assert isinstance(data[0]["year"], int)
        assert isinstance(data[0]["thefts"], int)


def test_thefts_nonexistent_postcode():
    postcode = "9999"
    response = requests.get(f"{BASE_URL}/api/v1/postcode/{postcode}/thefts")
    assert response.status_code == 404


def test_thefts_invalid_postcode_format():
    for bad_postcode in ["abcd", "37a7", "12-34"]:
        response = requests.get(f"{BASE_URL}/api/v1/postcode/{bad_postcode}/thefts")
        assert response.status_code == 422


def test_thefts_empty_postcode():
    response = requests.get(f"{BASE_URL}/api/v1/postcode//thefts")
    assert response.status_code == 200
    data = response.json()
    assert "detail" in data


def test_thefts_missing_postcode():
    response = requests.get(f"{BASE_URL}/api/v1/postcode/thefts")
    assert response.status_code == 200
    data = response.json()
    assert "detail" in data


def test_thefts_postcode_with_spaces():
    postcode = "37 37"
    response = requests.get(f"{BASE_URL}/api/v1/postcode/{postcode}/thefts")
    assert response.status_code == 422


def test_thefts_postcode_numeric_edge_cases():
    for postcode in ["0000", "9999"]:
        response = requests.get(f"{BASE_URL}/api/v1/postcode/{postcode}/thefts")
        assert response.status_code == 404

def test_thefts_large_numeric_postcode():
    """Unrealistically large postcode returns 422."""
    response = requests.get(f"{BASE_URL}/api/v1/postcode/99999/thefts")
    assert response.status_code == 422


def test_thefts_boundary_postcode():
    """Known lowest VIC postcode (3000) should work (already tested, but explicit)."""
    response = requests.get(f"{BASE_URL}/api/v1/postcode/3000/thefts")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_thefts_malformed_symbols():
    """Malformed postcode returns structured error response."""
    response = requests.get(f"{BASE_URL}/api/v1/postcode/30@#/thefts")
    assert response.status_code == 200  # API returns 200 even for malformed
    data = response.json()
    # The response should have 'detail' key
    assert isinstance(data, dict)
    assert "detail" in data


def test_thefts_schema_validation():
    """Ensure schema keys match API: 'year' and 'thefts'."""
    response = requests.get(f"{BASE_URL}/api/v1/postcode/3000/thefts")
    assert response.status_code == 200
    data = response.json()
    for item in data:
        assert set(item.keys()) == {"year", "thefts"}
        assert isinstance(item["year"], int)
        assert isinstance(item["thefts"], int)

