import requests

BASE_URL = "http://localhost:8000"

def test_health():
    response = requests.get(f"{BASE_URL}/api/health")
    assert response.status_code == 200
    assert response.text == "ok"
