import requests
from urllib.parse import quote

BASE_URL = "http://localhost:8000"

def test_list_models_default():
    """Default list of models"""
    response = requests.get(f"{BASE_URL}/api/v1/models")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_list_models_limit_offset():
    """Test limit and offset"""
    params = {"limit": 5, "offset": 2}
    response = requests.get(f"{BASE_URL}/api/v1/models", params=params)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 5

def test_list_models_filter_brand():
    """Filter by brand"""
    params = {"brand": "Yamaha"}
    response = requests.get(f"{BASE_URL}/api/v1/models", params=params)
    assert response.status_code == 200
    data = response.json()
    for item in data:
        assert "Yamaha".lower() in item["brand"].lower()

def test_list_models_filter_model():
    """Filter by model"""
    params = {"model": "YZF-R3"}
    response = requests.get(f"{BASE_URL}/api/v1/models", params=params)
    assert response.status_code == 200
    data = response.json()
    for item in data:
        assert "YZF-R3".lower() in item["model"].lower()

def test_list_models_min_total():
    """Filter by minimum total thefts"""
    params = {"min_total": 10}
    response = requests.get(f"{BASE_URL}/api/v1/models", params=params)
    assert response.status_code == 200
    data = response.json()
    for item in data:
        assert item["total"] >= 10

def test_list_models_sorting():
    """Test sorting"""
    params = {"sort": "model"}
    response = requests.get(f"{BASE_URL}/api/v1/models", params=params)
    assert response.status_code == 200

def test_list_models_invalid_params():
    """Invalid parameters should return 422 or fallback"""
    params = {"limit": -1, "offset": -5, "min_total": -10}
    response = requests.get(f"{BASE_URL}/api/v1/models", params=params)
    assert response.status_code in (200, 422)

def test_model_details_nonexistent():
    response = requests.get(f"{BASE_URL}/api/v1/models/NotABrand/NotAModel")
    assert response.status_code == 404

def test_model_details_valid():
    list_response = requests.get(f"{BASE_URL}/api/v1/models", params={"limit": 1})
    assert list_response.status_code == 200
    models = list_response.json()
    if not models:
        return
    first_model = models[0]
    brand = first_model["brand"]
    model = first_model["model"]

    brand_encoded = quote(brand)
    model_encoded = quote(model)

    response = requests.get(f"{BASE_URL}/api/v1/models/{brand_encoded}/{model_encoded}")
    if response.status_code == 404:
        return
    assert response.status_code == 200
    data = response.json()
    assert data["brand"] == brand
    assert data["model"] == model





