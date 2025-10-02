import requests

BASE_URL = "http://localhost:8000"

def check_address_fields(item):
    """Helper to validate address dict structure and types"""
    assert "address" in item
    assert "postcode" in item
    assert "suburb" in item
    assert isinstance(item["address"], str)
    assert isinstance(item["postcode"], str)
    assert isinstance(item["suburb"], str)

# ----------------------
# Success cases
# ----------------------
def test_address_valid_postcode():
    """Valid postcode should return a list of addresses with correct fields"""
    postcode = "3000"
    response = requests.get(f"{BASE_URL}/api/v1/postcode/{postcode}/addresses")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for item in data:
        check_address_fields(item)

def test_address_postcode_with_spaces():
    """Postcode with leading/trailing spaces should return correct addresses"""
    postcode = " 3000 "
    response = requests.get(f"{BASE_URL}/api/v1/postcode/{postcode.strip()}/addresses")
    assert response.status_code == 200
    data = response.json()
    for item in data:
        check_address_fields(item)

# ----------------------
# Edge / invalid input
# ----------------------
def test_address_nonexistent_postcode():
    """Nonexistent postcode should return empty list or 404 with detail"""
    postcode = "9999"
    response = requests.get(f"{BASE_URL}/api/v1/postcode/{postcode}/addresses")
    assert response.status_code in (200, 404)
    data = response.json()
    if response.status_code == 200:
        assert isinstance(data, list)
        assert len(data) == 0
    else:
        assert "detail" in data

def test_address_invalid_postcode_format():
    """Invalid postcode format should return 422 with validation detail"""
    postcode = "abcd"
    response = requests.get(f"{BASE_URL}/api/v1/postcode/{postcode}/addresses")
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

def test_address_empty_postcode():
    """Empty postcode string returns Not Found message"""
    postcode = ""
    response = requests.get(f"{BASE_URL}/api/v1/postcode/{postcode}/addresses")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data.get("detail") == "Not found"

def test_address_missing_postcode():
    """Missing postcode in URL returns Not Found message"""
    response = requests.get(f"{BASE_URL}/api/v1/postcode//addresses")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data.get("detail") == "Not found"

def test_address_long_postcode():
    """Very long numeric postcode should be handled gracefully"""
    postcode = "1" * 50
    response = requests.get(f"{BASE_URL}/api/v1/postcode/{postcode}/addresses")
    assert response.status_code in (200, 422, 404)


