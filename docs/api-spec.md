# API Specification – Hotspot Parking App

## Overview
This document defines the REST API endpoints for the Hotspot app.

The API allows riders to:

- Search for safe parking by suburb/postcode
- View motorcycle theft risk scores by location
- Compare motorcycle models by theft risk
- Analyze risk data by Local Government Area (LGA)
- Get comprehensive theft statistics

**Base URL:** `/api/v1`

---
## 1.0 Health Check
### 1.1 System Health
**Endpoint:**
`GET /health`

**Request Example:**
`GET /health`

**Response Example:**
`ok`

## 2.0 Parking Safety Search & Discovery

### 2.1 Search for Safe Parking
**Endpoint:**
`GET /search`

**Query Parameters:**
- `q` (string, required) -> search query for suburb or postcode

**Request Example:**
`GET /search?q=Richmond`

**Response Example:**
```json
[
  {
    "label": "Richmond, 3121",
    "suburb": "Richmond",
    "postcode": "3121",
    "lga": "Yarra City",
    "risk_score": 0.025476
  },
  {
    "label": "Richmond North, 3121",
    "suburb": "Richmond North",
    "postcode": "3121",
    "lga": "Yarra City",
    "risk_score": 0.025476
  }
]
```
### 2.2 Submit Parking Suggestion
**Endpoint:**
`POST /parking`

**Request Body:**
```json
  {
    "address": "Richmond, 3121",
    "suburb": "Richmond",
    "postcode": "3121",
    "type": "off-street",
    "lighting": 4,
    "cctv": true,
    "facilities": [1, 2]
  }

```
**Response Example:**
```json
{
  "parking_id": 101,
  "message": "Parking suggestion submitted successfully"
}
```

### 2.3 Get Parking by Postcode
**Endpoint:**
`GET /parking/{postcode}`

**Path Parameters:**
- `{postcode}` (string, required) -> postcode to search for parking options

**Request Example:**
`GET /parking/3121`

**Response Example:**
```json
[
  {
    "parking_id": 101,
    "address": "123 Example St",
    "suburb": "Richmond",
    "postcode": "3121",
    "type": "off-street",
    "lighting": 4,
    "cctv": true,
    "created_at": "2025-09-19T16:46:31.212339",
    "facilities": [
      {"facility_id": 1, "facility_name": "Covered parking"},
      {"facility_id": 2, "facility_name": "Security guard"}
    ]
  }
]
```

## 3.0 Risk Analysis

### 3.1 Compare Risk for Postcode
**Endpoint:**
`GET /risk/compare`

**Query Parameters:**
- `postcode` (string, required) -> postcode to analyse

**Request Example:**
`GET /risk/compare?postcode=3121`

**Response Example:**
```json
{
  "base": {
    "postcode": "3121",
    "suburb": "Richmond",
    "lga": "Yarra City",
    "motorcycle_theft_rate": 2.547619,
    "risk_score": 0.025476
  },
  "defaults": {
    "default_risk": 0.014285,
    "max_risk": 0.125000
  }
}
```

### 3.2 Top Risk Areas
**Endpoint:**
`GET /risk/top`

**Query Parameters:**
- `scope` (string, optional) -> `postcode` | `lga` (default: `postcode`)
- `order` (string, optional) -> `desc` | `asc` (default: `desc`)
- `limit` (integer, optional) -> 1-200 (default: 20)

**Request Example:**
`GET /risk/top?scope=postcode&order=desc&limit=10`

**Response Example:**
```json
[
  {
    "postcode": "3000",
    "suburb": "Melbourne",
    "lga": "Melbourne City",
    "risk_score": 0.125000
  },
  {
    "postcode": "3141",
    "suburb": "South Yarra",
    "lga": "Stonnington City",
    "risk_score": 0.098765
  }
]
```

## 4.0 Motorcycle Model Risk

### 4.1 List Motorcycle Models by Risk
**Endpoint:**
`GET /models`
  
**Query Parameters:**
- `brand` (string, optional) -> filter by brand name
- `model` (string, optional) -> filter by model name
- `min_total` (integer, optional) -> minimum total thefts (default: 0)
- `sort` (string, optional) -> `risk_desc` | `risk_asc` | `total_desc` | `total_asc` | `brand` | `model` (default: `risk_desc`)
- `limit` (integer, optional) -> 1-500 (default: 100)
- `offset` (integer, optional) -> pagination offset (default: 0)

**Request Example:**
`GET /models?brand=honda&sort=risk_desc&limit=5`

**Response Example:**
```json
[
  {
    "brand": "honda",
    "model": "cbr650",
    "total": 17,
    "percentage": 0.06073380729520203,
    "model_risk": 0.01484327087198516
  }
]
```

### 4.2 Get Specific Model Risk
**Endpoint:**
`GET /models/{brand}/{model}`

**Path Parameters:**
- `{brand}` (string, required) -> motorcycle brand
- `{model}` (string, required) -> motorcycle model

**Request Example:**
`GET /models/honda/cbr1000rr`

**Response Example:**
```json
{
  "brand": "honda",
  "model": "cbr650",
  "total": 17,
  "percentage": 0.06073380729520203,
  "model_risk": 0.01484327087198516
}
```

## 5.0 Local Government Area (LGA) Analysis

### 5.1 LGA Risk Summary
**Endpoint:**
`GET /lgas`

**Query Parameters:**
- `q` (string, optional) -> filter by LGA name
- `sort` (string, optional) -> `avg_desc` | `avg_asc` | `count_desc` | `count_asc` | `lga` (default: `avg_desc`)

**Request Example:**
`GET /lgas?q=Melbourne&sort=avg_desc`

**Response Example:**
```json
[
  {
    "lga": "Melbourne",
    "postcode_count": 20,
    "avg_risk": 0.632164,
    "min_risk": 0.6321638896707255,
    "max_risk": 0.6321638896707255
  }
]
```

### 5.2 LGA Postcode Details
**Endpoint:**
`GET /lgas/{lga}/postcodes`

**Path Parameters:**
- `{lga}` (string, required) -> Local Government Area name

**Query Parameters:**
- `order` (string, optional) -> `desc` | `asc` (default: `desc`)

**Request Example:**
`GET /lgas/Melbourne City/postcodes?order=desc`

**Response Example:**
```json
[
  {
    "postcode": "3000",
    "suburb": "MELBOURNE",
    "long": 144.9825846,
    "lat": -37.81443733,
    "risk_score": 0.6321638896707255
  },
  {
    "postcode": "3002",
    "suburb": "EAST MELBOURNE",
    "long": 144.9825846,
    "lat": -37.81443733,
    "risk_score": 0.6321638896707255
  }
]
```
## 6.0 Address Lookup

### 6.1 Get Addresses by Postcode
**Endpoint:**
`GET /addresses/{postcode}`

**Path Parameters:**
- `{postcode}` (string, required) -> postcode to filter addresses

**Query Parameters:**
- `q` (string, optional) -> search query to filter addresses within the postcode

**Request Example:**
`GET /addresses/3000?q=Collins`

**Response Example:**
```json
[
  {
    "address": "123 Collins St",
    "suburb": "Melbourne",
    "postcode": "3000"
  },
  {
    "address": "456 Collins St",
    "suburb": "Melbourne",
    "postcode": "3000"
  }
]
```
## 7.0 Statistics

### 7.1 Overall Statistics Summary
**Endpoint:**
`GET /stats/summary`

**Request Example:**
`GET /stats/summary`

**Response Example:**
```json
{
  "total_postcodes": 3482,
  "total_lgas": 78,
  "avg_postcode_risk": 0.202648,
  "total_models": 1529
}
```

## 8.0 System

### 8.1 Health Check
**Endpoint:**
`GET /health`

**Request Example:**
`GET /health`

**Response:**
```
ok
```

## 9.0 Error Handling

### 9.1 Resource Not Found

**Response Example:**
```json
{
  "detail": "Postcode not found"
}
```

### 9.2 Invalid Parameters

**Response Example:**
```json
{
  "detail": "scope must be postcode or lga"
}
```
