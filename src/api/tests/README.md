# Hotspot API Tests

This directory contains automated tests for the **Hotspot API**, designed to validate endpoint functionality, response structure, input validation, and data integrity.

## Overview

The tests use **pytest** to perform automated verification of the Hotspot API. They cover:

- API health checks  
- Endpoint validation and data models  
- Postcode feeds and theft statistics  
- Risk calculations and search functionality  
- Platform-wide statistics  
- Contact form submissions  

---

## Test Structure

The `tests/` folder is organized as follows:

| File | Purpose |
|------|---------|
| `test_basic_endpoints.py` | Basic endpoint checks, e.g., root and version endpoints |
| `test_health.py` | Health check endpoint validation (`/api/health`) |
| `test_models.py` | Data model validation and schema consistency |
| `test_parking.py` | Tests for `/api/v1/parking` endpoint, including submissions and edge cases |
| `test_postcodes.py` | Tests for postcode feed endpoint (`/api/v1/postcode/{postcode}/feed`) |
| `test_risk.py` | Tests for risk scoring endpoints and calculations |
| `test_search.py` | Tests for search endpoints with query parameters and filters |
| `test_statistics.py` | Tests for platform summary statistics (`/api/v1/statistics/summary`) |
| `test_address.py` | Tests for address-related endpoints and validation |
| `test_thefts.py` | Tests for historical motorcycle theft statistics (`/api/v1/postcode/{postcode}/thefts`) |
| `test_contact.py` | Tests for contact or support endpoints, including form submissions |

---

## Running the Tests

**Run all tests**:

pytest -v

**Run a single test file**:

pytest -v tests/test_postcodes.py

**Run a single test function**:

pytest -v tests/test_thefts.py::test_thefts_valid_postcode
