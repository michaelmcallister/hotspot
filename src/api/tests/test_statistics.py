import requests

BASE_URL = "http://localhost:8000"

def test_statistics_summary_status_code():
    response = requests.get(f"{BASE_URL}/api/v1/statistics/summary")
    assert response.status_code == 200

def test_statistics_summary_structure():
    response = requests.get(f"{BASE_URL}/api/v1/statistics/summary")
    data = response.json()
    assert isinstance(data, dict)
    expected_keys = {"total_postcodes", "total_addresses", "total_lgas", "total_submissions"}
    assert expected_keys.issubset(data.keys())

def test_statistics_summary_types():
    response = requests.get(f"{BASE_URL}/api/v1/statistics/summary")
    data = response.json()
    
    assert isinstance(data.get("total_postcodes"), int)
    assert isinstance(data.get("total_addresses"), int)
    assert isinstance(data.get("total_lgas"), int)
    assert isinstance(data.get("total_submissions"), int)

def test_statistics_summary_non_empty():
    response = requests.get(f"{BASE_URL}/api/v1/statistics/summary")
    data = response.json()
    
    assert data.get("total_postcodes") >= 0
    assert data.get("total_addresses") >= 0
    assert data.get("total_lgas") >= 0
    assert data.get("total_submissions") >= 0

def test_statistics_summary_cache_consistency():
    response1 = requests.get(f"{BASE_URL}/api/v1/statistics/summary").json()
    response2 = requests.get(f"{BASE_URL}/api/v1/statistics/summary").json()
    assert response1 == response2
