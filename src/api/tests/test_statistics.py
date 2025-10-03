import requests

BASE_URL = "http://localhost:8000"

def test_statistics_summary_status_code():
    """Summary endpoint should return 200."""
    response = requests.get(f"{BASE_URL}/api/v1/statistics/summary")
    assert response.status_code == 200

def test_statistics_summary_structure():
    """Summary response should have expected keys."""
    response = requests.get(f"{BASE_URL}/api/v1/statistics/summary")
    data = response.json()
    assert isinstance(data, dict)
    expected_keys = {"total_postcodes", "total_addresses", "total_lgas", "total_submissions"}
    assert expected_keys.issubset(data.keys())

def test_statistics_summary_types():
    """Ensure each field is the correct type."""
    response = requests.get(f"{BASE_URL}/api/v1/statistics/summary")
    data = response.json()
    
    assert isinstance(data.get("total_postcodes"), int)
    assert isinstance(data.get("total_addresses"), int)
    assert isinstance(data.get("total_lgas"), int)
    assert isinstance(data.get("total_submissions"), int)

def test_statistics_summary_non_empty():
    """Check that numerical fields are non-negative."""
    response = requests.get(f"{BASE_URL}/api/v1/statistics/summary")
    data = response.json()
    
    assert data.get("total_postcodes") >= 0
    assert data.get("total_addresses") >= 0
    assert data.get("total_lgas") >= 0
    assert data.get("total_submissions") >= 0

def test_statistics_summary_cache_consistency():
    """Repeated calls return the same response (if caching)."""
    response1 = requests.get(f"{BASE_URL}/api/v1/statistics/summary").json()
    response2 = requests.get(f"{BASE_URL}/api/v1/statistics/summary").json()
    assert response1 == response2
