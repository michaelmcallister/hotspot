# Hotspot API

Community driven motorcycle parking suggestions for Victoria, Australia

# Base URL


| URL | Description |
|-----|-------------|
| https://hotspot.sknk.ws | Production server |


# APIs

## GET /api/health

Health check

Simple health check endpoint for monitoring




### Responses

#### 200


Returns 'ok' when service is running


string







## GET /api/v1/search

Search suburbs

Search for Victorian suburbs by name or postcode with risk scoring


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| q | string | True | Search term (suburb name or postcode) |


### Responses

#### 200


List of matching suburbs with risk scores


array







#### 422


Validation Error


[HTTPValidationError](#httpvalidationerror)







## GET /api/v1/statistics/summary

Get platform statistics

Returns aggregated platform-wide statistics including coverage and submission counts




### Responses

#### 200


Summary statistics with caching for performance


[StatisticsSummary](#statisticssummary)







## GET /api/v1/risk/top

Get risk rankings

Paginated list of suburbs or LGAs ranked by safety scores with search and sorting


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| scope | string | False | Group by postcode or lga |
| page | integer | False | Page number |
| itemsPerPage | integer | False | Results per page |
| sortBy | string | False | Column to sort by |
| sortOrder | string | False | Sort direction |
| search | string | False | Search filter text |


### Responses

#### 200


Paginated risk data with total count


[PaginatedRiskResponse](#paginatedriskresponse)







#### 422


Validation Error


[HTTPValidationError](#httpvalidationerror)







## GET /api/v1/models

List motorcycle models

Search and filter motorcycle models with theft risk data


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| brand |  | False | Filter by brand name |
| model |  | False | Filter by model name |
| min_total | integer | False | Minimum total theft count |
| sort | string | False | Sort order |
| limit | integer | False | Maximum results to return |
| offset | integer | False | Number of results to skip |


### Responses

#### 200


List of motorcycle models with risk scores


array







#### 422


Validation Error


[HTTPValidationError](#httpvalidationerror)







## GET /api/v1/models/{brand}/{model}

Get motorcycle details

Get detailed theft risk data for a specific motorcycle model


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| brand | string | True | Motorcycle brand name |
| model | string | True | Motorcycle model name |


### Responses

#### 200


Motorcycle model with complete theft statistics


[MotorcycleModel](#motorcyclemodel)







#### 422


Validation Error


[HTTPValidationError](#httpvalidationerror)







## GET /api/v1/postcode/{postcode}/addresses

Get addresses by postcode

Retrieve validated Victorian addresses for a specific postcode with optional search filtering


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| postcode | string | True | Victorian postcode |
| q |  | False | Filter addresses by partial match |


### Responses

#### 200


List of matching addresses with full details


array







#### 422


Validation Error


[HTTPValidationError](#httpvalidationerror)







## POST /api/v1/parking

Submit parking location

Submit a community contributed safe parking location. Address must be valid Victorian address.




### Request Body

[ParkingSubmissionRequest](#parkingsubmissionrequest)







### Responses

#### 200


Confirmation of parking submission with unique ID


[ParkingSubmissionResponse](#parkingsubmissionresponse)







#### 422


Validation Error


[HTTPValidationError](#httpvalidationerror)







## POST /api/v1/contact

Submit contact form

Submit feedback or report issues. Creates GitHub issue for tracking. Requires reCAPTCHA verification.




### Request Body

[ContactFormSubmission](#contactformsubmission)







### Responses

#### 200


Success confirmation


[ContactFormResponse](#contactformresponse)







#### 422


Validation Error


[HTTPValidationError](#httpvalidationerror)







## GET /api/v1/postcode/{postcode}/feed

Get postcode feed

Returns parking submissions and nearby safer suburbs for a given postcode


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| postcode | string | True | Victorian postcode |


### Responses

#### 200


Feed data including current location info, parking spots, and safer alternatives


[PostcodeFeedResponse](#postcodefeedresponse)







#### 422


Validation Error


[HTTPValidationError](#httpvalidationerror)







## GET /api/v1/postcode/{postcode}/thefts

Get theft statistics

Historical motorcycle theft data by year for a specific postcode


### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| postcode | string | True | Victorian postcode |


### Responses

#### 200


List of yearly theft counts


array







#### 422


Validation Error


[HTTPValidationError](#httpvalidationerror)







## GET /

Read Index





### Responses

#### 200


Successful Response








## GET /{full_path}

Catch All



### Parameters

| Name | Type | Required | Description |
|------|------|----------|-------------|
| full_path | string | True |  |


### Responses

#### 200


Successful Response








#### 422


Validation Error


[HTTPValidationError](#httpvalidationerror)







# Components



## Address


Victorian address


| Field | Type | Description |
|-------|------|-------------|
| address | string | Full street address |
| suburb | string | Suburb name |
| postcode | string | 4-digit postcode |


## ContactFormResponse


Contact form submission response


| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Whether submission was successful |


## ContactFormSubmission


Contact form submission request


| Field | Type | Description |
|-------|------|-------------|
| email | string | Contact email address |
| category | string | Issue category |
| subject | string | Issue subject |
| postcode |  | Related postcode |
| details | string | Issue details |
| recaptchaToken | string | reCAPTCHA verification token |


## CurrentLocation


Current postcode information


| Field | Type | Description |
|-------|------|-------------|
| postcode | string | 4-digit postcode |
| suburb | string | Suburb name |
| risk_score | number | Risk score from 0 (safe) to 1 (high risk) |


## HTTPValidationError



| Field | Type | Description |
|-------|------|-------------|
| detail | array |  |


## MotorcycleModel


Motorcycle model with theft statistics


| Field | Type | Description |
|-------|------|-------------|
| brand | string | Motorcycle brand |
| model | string | Model name |
| total | integer | Total number of thefts |
| percentage | number | Percentage of total thefts |
| model_risk | number | Risk score from 0 (safe) to 1 (high risk) |


## PaginatedRiskResponse


Paginated risk ranking response


| Field | Type | Description |
|-------|------|-------------|
| items | array | Risk ranking items |
| total | integer | Total number of items |


## ParkingFacility


Parking facility details


| Field | Type | Description |
|-------|------|-------------|
| facility_id | integer | Unique facility identifier |
| facility_name | string | Facility name |


## ParkingSubmission


Community submitted parking location


| Field | Type | Description |
|-------|------|-------------|
| parking_id | integer | Unique parking submission ID |
| address | string | Street address |
| suburb | string | Suburb name |
| postcode | string | 4-digit postcode |
| type | string | Parking type: on-street, off-street, or secure |
| lighting |  | Lighting quality: 1=poor to 4=excellent |
| cctv |  | CCTV availability |
| facilities | array | Available facilities at location |
| created_at |  | Submission timestamp |


## ParkingSubmissionRequest


Request model for submitting parking location


| Field | Type | Description |
|-------|------|-------------|
| address | string | Street address |
| suburb | string | Suburb name |
| postcode | string | Postcode |
| type | string | Parking type |
| lighting |  | Lighting quality: 1=poor, 2=fair, 3=good, 4=excellent |
| cctv |  | CCTV availability: true, false, or null for unknown |
| facilities |  | List of facility IDs |


## ParkingSubmissionResponse


Response model for parking submission


| Field | Type | Description |
|-------|------|-------------|
| parking_id | integer | Unique parking submission ID |
| message | string | Success message |
| action | string | Action performed: inserted, updated, or no_change |


## PostcodeFeedResponse


Feed data for a specific postcode


| Field | Type | Description |
|-------|------|-------------|
| current |  | Current location details |
| parking_submissions | array | Community parking submissions |
| nearest_safer_suburbs | array | Nearby suburbs with lower risk |


## SaferSuburb


Nearby suburb with lower risk score


| Field | Type | Description |
|-------|------|-------------|
| postcode | string | 4-digit postcode |
| suburb | string | Suburb name |
| lga | string | Local government area |
| distance_in_meters | integer | Distance from target postcode in meters |
| risk_score | number | Risk score from 0 (safe) to 1 (high risk) |
| parking_count | integer | Number of community parking submissions |


## StatisticsSummary


Platform-wide statistics


| Field | Type | Description |
|-------|------|-------------|
| total_postcodes | integer | Number of postcodes covered |
| total_addresses | integer | Number of validated addresses |
| total_lgas | integer | Number of local government areas |
| total_submissions | integer | Number of community submissions |


## SuburbSearchResult


Search result for suburb lookup


| Field | Type | Description |
|-------|------|-------------|
| label | string | Display label combining suburb and postcode |
| suburb | string | Suburb name |
| postcode | string | 4-digit postcode |
| lga | string | Local government area |
| risk_score | number | Risk score from 0 (safe) to 1 (high risk) |


## ValidationError



| Field | Type | Description |
|-------|------|-------------|
| loc | array |  |
| msg | string |  |
| type | string |  |


## YearlyTheft


Yearly theft statistics


| Field | Type | Description |
|-------|------|-------------|
| year | integer | Calendar year |
| thefts | integer | Number of reported thefts |
