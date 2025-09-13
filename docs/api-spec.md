# API Specification – Hotspot Parking App

## Overview
This document defines the REST API endpoints for the Hotspot app.

The API allows riders to:

- Search for safe parking by suburb/postcode
- Filter by parking type
- Suggest/report a parking spot
- Upvote/downvote suggestions
- Get directions to a spot
- Save favourite parking spots for easy access

**Base URL:** `/api/v1`

---

## 1.0 Parking Search & Discovery (Epic 5.0)

### 1.1 Search for Parking
**Endpoint:**  
`GET /parking`

**Query Parameters:**  
- `suburb` (string, required) -> suburb or postcode  
- `type` (string, optional) -> `on-street` | `off-street` | `secure`

**Request Example:**
`GET /parking?suburb=Richmond&type=secure`

**Response Example:**
```json
[
  {
    "id": 1,
    "suburb": "Richmond",
    "type": "secure",
    "lat": -37.82,
    "long": 144.99,
    "votes": 5
  },
  {
    "id": 2,
    "suburb": "Richmond",
    "type": "on-street",
    "lat": -37.83,
    "long": 145.01,
    "votes": 2
  }
]
```

### 1.2 Get Parking Spot by ID
**Endpoint:**  
`GET /parking/{id}`

**Path Parameters:**  
- `{id}` (integer, required) -> unique parking spot ID

**Request Example:**
`GET /parking/1`

**Response Example:**
```json
{
  "id": 1,
  "suburb": "Richmond",
  "type": "secure",
  "lat": -37.82,
  "long": 144.99,
  "votes": 5,
  "created_at": "2025-09-10T10:00:00Z"
}
```

### 1.3 Get Directions via Google Maps
**Endpoint:**  
`GET /parking/{id}/directions`

**Path Parameters:**  
- `{id}` (integer, required) -> parking spot ID

**Query Parameters (optional):**  
- `from` (string) -> user starting location in lat,long format

**Request Example:**
`GET /parking/1/directions?from=-37.81,144.97`

**Response Example:**
```json
{
  "id": 1,
  "from": [-37.81, 144.97],
  "to": [-37.82, 144.99],
  "directions_url": "https://maps.app.goo.gl/QnP8Z1coeH3h2R236"
}
```

## 2.0 User Supplied Content (Epic 4.0)

### 2.1 Suggest a Parking Spot

**Endpoint:**  
`POST /parking`

**Request Example:**
```json
{
  "suburb": "Brunswick",
  "type": "on-street",
  "lat": -37.77,
  "long": 144.96
}
```

**Response Example:**
```json
{
  "message": "Parking spot added successfully",
  "id": 3
}
```

### 2.2 Upvote/Downvote a Spot

**Endpoint:**  
`POST /parking/{id}/vote`

**Path Parameters:**  
- `{id}` (integer, required) -> parking spot ID

**Request Example:**
```json
{ "vote": "up" }  // or "down"
```

**Response Example:**
```json
{
  "id": 3,
  "votes": 6
}
```

### 2.3 Save Favourite Spots

**Endpoint:**  
`POST /users/{id}/favourites`

**Path Parameters:**  
- `{id}` (integer, required) -> user ID

**Request Example:**
```json
{ "parking_id": 1 }
```

**Response Example:**
```json
{
  "message": "Parking spot saved to favourites",
  "user_id": 13,
  "parking_id": 1
}
```

## 3.0 Error Handling

### 3.1 Invalid suburb parameter

**Response Example:**
```json
{
  "error": "Invalid suburb parameter",
  "status": 400
}
```
### 3.2 Invalid parking id parameter

**Response Example:**
```json
{
  "error": "Parking spot not found",
  "status": 404
}
```