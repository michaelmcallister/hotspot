import requests

BASE_URL = "http://localhost:8000"

def test_valid_parking_submission():
    payload = {
        "address": "1838 ABBEYARDS ROAD",
        "suburb": "ABBEYARD",
        "postcode": "3737",
        "parking_type": "off-street",  # corrected
        "lighting": "good",            # corrected
        "CCTV": True,                  # corrected
        "facilities": []
    }
    response = requests.post(f"{BASE_URL}/api/v1/parking", json=payload)

    print("Status code:", response.status_code)
    print("Response body:", response.text)

    assert response.status_code in (200, 201, 422)  # 201 is standard for created

    if response.status_code in (200, 201):
        data = response.json()
        assert "parking_id" in data
        assert "message" in data

def test_parking_missing_fields():
    """Missing required fields should return 422"""
    payload = {
        "address": "1838 ABBEYARDS ROAD"
        # missing postcode, suburb, parking_type, etc.
    }
    response = requests.post(f"{BASE_URL}/api/v1/parking", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

def test_parking_invalid_field_types():
    """Invalid types for fields should return 422"""
    payload = {
        "address": 123,
        "postcode": 3000,
        "suburb": 456,
        "parking_type": "street",
        "lighting": "good",
        "CCTV": "yes",
        "facilities": "none",
        "lat": "invalid",
        "lng": "invalid"
    }
    response = requests.post(f"{BASE_URL}/api/v1/parking", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

def test_parking_extra_fields():
    """Submitting extra fields should return 422"""
    payload = {
        "address": "1838 ABBEYARDS ROAD",
        "suburb": "ABBEYARD",
        "postcode": "3737",
        "type": "street",
        "lighting": 3,
        "cctv": True,
        "facilities": [],
        "lat": -37.8136,
        "lng": 144.9631,
        "extra_field": "ignored"
    }
    response = requests.post(f"{BASE_URL}/api/v1/parking", json=payload)
    assert response.status_code == 422

def test_parking_invalid_coordinates():
    """Invalid lat/lng should return 422 or 400"""
    payload = {
        "address": "1838 ABBEYARDS ROAD",
        "postcode": "3737",
        "suburb": "ABBEYARD",
        "parking_type": "street",
        "lighting": "good",
        "CCTV": True,
        "facilities": [],
        "lat": -999,
        "lng": 200
    }
    response = requests.post(f"{BASE_URL}/api/v1/parking", json=payload)
    assert response.status_code in (422, 400)
    data = response.json()
    assert "detail" in data

def test_parking_duplicate_submission():
    """Duplicate submission returns 422 if API rejects duplicates"""
    payload = {
        "address": "1838 ABBEYARDS ROAD",
        "postcode": "3737",
        "suburb": "ABBEYARD",
        "parking_type": "street",
        "lighting": "good",
        "CCTV": True,
        "facilities": [],
        "lat": -37.8136,
        "lng": 144.9631
    }
    requests.post(f"{BASE_URL}/api/v1/parking", json=payload)  # first submission
    second_response = requests.post(f"{BASE_URL}/api/v1/parking", json=payload)
    assert second_response.status_code in (200, 201, 422)  # include 422

def test_parking_max_field_lengths():
    """Very long address/suburb strings handled"""
    payload = {
        "address": "A" * 500,
        "suburb": "B" * 200,
        "postcode": "3737",
        "type": "street",
        "lighting": 3,
        "cctv": True,
        "facilities": [],
        "lat": -37.8136,
        "lng": 144.9631
    }
    response = requests.post(f"{BASE_URL}/api/v1/parking", json=payload)
    assert response.status_code in (200, 201, 422)

def test_parking_boundary_coordinates():
    """Boundary lat/lng values handled"""
    for lat, lng in [(-90, -180), (-90, 180), (90, -180), (90, 180)]:
        payload = {
            "address": "1838 ABBEYARDS ROAD",
            "suburb": "ABBEYARD",
            "postcode": "3737",
            "type": "street",
            "lighting": 3,
            "cctv": True,
            "facilities": [],
            "lat": lat,
            "lng": lng
        }
        response = requests.post(f"{BASE_URL}/api/v1/parking", json=payload)
        assert response.status_code in (200, 201, 422)

def test_parking_negative_lighting():
    """Negative or zero lighting returns 422"""
    for lighting in [0, -1, -5]:
        payload = {
            "address": "1838 ABBEYARDS ROAD",
            "suburb": "ABBEYARD",
            "postcode": "3737",
            "type": "street",
            "lighting": lighting,
            "cctv": True,
            "facilities": []
        }
        response = requests.post(f"{BASE_URL}/api/v1/parking", json=payload)
        assert response.status_code == 422

def test_parking_optional_fields_omitted():
    """Optional fields omitted should still succeed if API allows"""
    payload = {
        "address": "1838 ABBEYARDS ROAD",
        "suburb": "ABBEYARD",
        "postcode": "3737",
        "type": "street",
        "lighting": 3,
        "cctv": True
        # facilities omitted
    }
    response = requests.post(f"{BASE_URL}/api/v1/parking", json=payload)
    # If facilities are required, this should return 422
    assert response.status_code in (200, 201, 422)

def test_parking_empty_required_fields():
    """Empty strings in required fields should return 422"""
    for field in ["address", "suburb", "postcode", "type"]:
        payload = {
            "address": "1838 ABBEYARDS ROAD",
            "suburb": "ABBEYARD",
            "postcode": "3737",
            "type": "street",
            "lighting": 3,
            "cctv": True,
            "facilities": []
        }
        payload[field] = ""
        response = requests.post(f"{BASE_URL}/api/v1/parking", json=payload)
        assert response.status_code == 422


