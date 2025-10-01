from fastapi import APIRouter, Request, HTTPException, Path
from typing import List
from models import PostcodeFeedResponse, YearlyTheft, ParkingSubmission, SaferSuburb, CurrentLocation, ParkingFacility

router = APIRouter(tags=["Postcodes"])

@router.get(
    "/v1/postcode/{postcode}/feed",
    summary="Get postcode feed",
    description="Returns parking submissions and nearby safer suburbs for a given postcode",
    response_description="Feed data including current location info, parking spots, and safer alternatives",
    response_model=PostcodeFeedResponse
)
def get_postcode_feed(
    request: Request,
    postcode: str = Path(..., description="Victorian postcode", pattern="^[0-9]{4}$")
) -> PostcodeFeedResponse:
    db = request.app.state.db

    target_postcode = db.fetch_all("""
        SELECT postcode, locality AS suburb, postcode_risk AS risk_score
        FROM postcode_risk
        WHERE postcode = :postcode
        LIMIT 1
    """, {"postcode": postcode})

    if not target_postcode:
        raise HTTPException(status_code=404, detail=f"Postcode {postcode} not found")

    current_risk_score = target_postcode[0]['risk_score']
    current_suburb = target_postcode[0]['suburb']

    parking_submissions = db.get_parking_by_postcode(postcode)

    for submission in parking_submissions:
        submission['facilities'] = db.get_facilities_for_parking(submission['parking_id'])

    # High Risk: risk > 0.5
    # Medium Risk: 0.2 < risk <= 0
    # Low Risk: risk <= 0.2

    if current_risk_score > 0.5:
        max_risk = 0.5
    elif current_risk_score > 0.2:
        max_risk = 0.2
    else:
        max_risk = current_risk_score

    nearest_suburbs_query = db.fetch_all("""
        SELECT
            pd.secondary_postcode as postcode,
            pr.locality as suburb,
            pr.local_government_area as lga,
            pd.distance_meters as distance_in_meters,
            pr.postcode_risk as risk_score
        FROM postcode_distances pd
        JOIN postcode_risk pr ON pd.secondary_postcode = pr.postcode
        WHERE pd.primary_postcode = :postcode
        AND pr.postcode_risk < :max_risk
        ORDER BY pd.distance_meters ASC
        LIMIT 20
    """, {
        "postcode": postcode,
        "max_risk": max_risk
    })

    for suburb_data in nearest_suburbs_query:
        try:
            parking_data = db.get_parking_by_postcode(suburb_data['postcode'])
            suburb_data['parking_count'] = len(parking_data) if parking_data else 0
        except:
            suburb_data['parking_count'] = 0

    parking_models = []
    for submission in parking_submissions:
        facilities = [ParkingFacility(**f) for f in submission.get('facilities', [])]
        parking_models.append(ParkingSubmission(
            **{k: v for k, v in submission.items() if k != 'facilities'},
            facilities=facilities
        ))

    safer_suburb_models = [SaferSuburb(**suburb) for suburb in nearest_suburbs_query]

    return PostcodeFeedResponse(
        current=CurrentLocation(
            postcode=postcode,
            suburb=current_suburb,
            risk_score=current_risk_score
        ),
        parking_submissions=parking_models,
        nearest_safer_suburbs=safer_suburb_models
    )

@router.get(
    "/v1/postcode/{postcode}/thefts",
    summary="Get theft statistics",
    description="Historical motorcycle theft data by year for a specific postcode",
    response_description="List of yearly theft counts",
    response_model=List[YearlyTheft]
)
def get_postcode_thefts(
    request: Request,
    postcode: str = Path(..., description="Victorian postcode", pattern="^[0-9]{4}$")
) -> List[YearlyTheft]:
    db = request.app.state.db

    postcode_exists = db.fetch_all("""
        SELECT postcode FROM postcode_yearly_thefts WHERE postcode = :postcode LIMIT 1
    """, {"postcode": postcode})

    if not postcode_exists:
        raise HTTPException(status_code=404, detail=f"No theft data found for postcode {postcode}")

    theft_data = db.fetch_all("""
        SELECT
            year,
            yearly_thefts as thefts
        FROM postcode_yearly_thefts
        WHERE postcode = :postcode
        ORDER BY year ASC
    """, {"postcode": postcode})

    return [YearlyTheft(year=int(record['year']), thefts=int(record['thefts'])) for record in theft_data]
