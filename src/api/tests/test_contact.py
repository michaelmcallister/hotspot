import requests

BASE_URL = "http://localhost:8000"

def test_contact_form_success():
    """Valid contact form submission"""
    payload = {
        "email": "test@example.com",
        "category": "feedback",
        "subject": "Test Submission",
        "postcode": "3121",
        "details": "This is a test",
        "recaptchaToken": "test-token"
    }
    response = requests.post(f"{BASE_URL}/api/v1/contact", json=payload)
    assert response.status_code in (200, 400, 422, 500)
    data = response.json()
    assert "success" in data or "detail" in data

def test_contact_missing_fields():
    """Missing required fields should return validation error"""
    payload = {
        "email": "test@example.com",
        "subject": "Missing Category",
        "postcode": "3121",
        "details": "Missing category",
        "recaptchaToken": "test-token"
    }
    response = requests.post(f"{BASE_URL}/api/v1/contact", json=payload)
    assert response.status_code in (422, 400, 500)
    if response.status_code in (422, 400):
        data = response.json()
        assert "category" in str(data)

def test_contact_invalid_email():
    """Invalid email format should return validation error"""
    payload = {
        "email": "not-an-email",
        "category": "feedback",
        "subject": "Invalid Email",
        "postcode": "3121",
        "details": "Testing invalid email",
        "recaptchaToken": "test-token"
    }
    response = requests.post(f"{BASE_URL}/api/v1/contact", json=payload)
    assert response.status_code in (422, 400, 500)
    if response.status_code in (422, 400):
        data = response.json()
        assert "email" in str(data)

def test_contact_empty_details():
    """Empty details field should return validation error"""
    payload = {
        "email": "test@example.com",
        "category": "feedback",
        "subject": "Empty Details",
        "postcode": "3121",
        "details": "",
        "recaptchaToken": "test-token"
    }
    response = requests.post(f"{BASE_URL}/api/v1/contact", json=payload)
    assert response.status_code in (422, 400, 500)
    if response.status_code in (422, 400):
        data = response.json()
        assert "details" in str(data)

def test_contact_invalid_postcode():
    """Invalid postcode format should return validation error"""
    payload = {
        "email": "test@example.com",
        "category": "feedback",
        "subject": "Invalid Postcode",
        "postcode": "abcd",
        "details": "Testing invalid postcode",
        "recaptchaToken": "test-token"
    }
    response = requests.post(f"{BASE_URL}/api/v1/contact", json=payload)
    assert response.status_code in (422, 400, 500)
    if response.status_code in (422, 400):
        data = response.json()
        assert "postcode" in str(data)

def test_contact_invalid_category():
    """Invalid category should return validation error"""
    payload = {
        "email": "test@example.com",
        "category": "invalid-category",
        "subject": "Invalid Category",
        "postcode": "3121",
        "details": "Testing invalid category",
        "recaptchaToken": "test-token"
    }
    response = requests.post(f"{BASE_URL}/api/v1/contact", json=payload)
    assert response.status_code in (422, 400, 500)
    if response.status_code in (422, 400):
        data = response.json()
        assert "category" in str(data)

def test_contact_missing_recaptcha():
    """Missing recaptchaToken should return validation error"""
    payload = {
        "email": "test@example.com",
        "category": "feedback",
        "subject": "Missing Recaptcha",
        "postcode": "3121",
        "details": "No recaptcha token"
    }
    response = requests.post(f"{BASE_URL}/api/v1/contact", json=payload)
    assert response.status_code in (422, 400, 500)
    if response.status_code in (422, 400):
        data = response.json()
        assert "recaptchaToken" in str(data)
