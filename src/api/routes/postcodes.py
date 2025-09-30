from fastapi import APIRouter, Request, HTTPException
from typing import List, Dict, Any

router = APIRouter()

@router.get("/v1/postcode/{postcode}/feed")
def get_postcode_feed(request: Request, postcode: str) -> Dict[str, Any]:
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

    return {
        "current": {
            "postcode": postcode,
            "suburb": current_suburb,
            "risk_score": current_risk_score
        },
        "parking_submissions": parking_submissions,
        "nearest_safer_suburbs": nearest_suburbs_query
    }

@router.get("/v1/postcode/{postcode}/thefts")
def get_postcode_thefts(request: Request, postcode: str) -> List[Dict[str, Any]]:
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

    # Ensure all values are integers
    for record in theft_data:
        record['year'] = int(record['year'])
        record['thefts'] = int(record['thefts'])

    return theft_data
