from fastapi.testclient import TestClient
from main import app
import os
os.environ["SQLITE_DB_PATH"] = "/Users/samanthamarriott/Documents/hotspot/src/data/hotspot.db"

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200

def test_search_endpoint():
    response = client.get("/api/v1/search?q=test")
    assert response.status_code == 200

def test_parking_postcode():
    response = client.get("/api/v1/parking/3000")  
    assert response.status_code == 200

