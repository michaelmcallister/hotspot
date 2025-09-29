from fastapi import APIRouter, Request, HTTPException
from typing import List, Dict, Any

router = APIRouter()

@router.get("/v1/postcode/{postcode}/nearest")
def get_nearest_postcodes(request: Request, postcode: str) -> List[Dict[str, Any]]:
    db = request.app.state.db

    target_exists = db.fetch_all("""
        SELECT postcode FROM postcode_risk WHERE postcode = :postcode LIMIT 1
    """, {"postcode": postcode})

    if not target_exists:
        raise HTTPException(status_code=404, detail=f"Postcode {postcode} not found")

    nearest_postcodes = db.fetch_all("""
        SELECT
            pd.secondary_postcode as postcode,
            pr.locality as suburb,
            pr.local_government_area as lga,
            pd.distance_meters as distance_in_meters,
            pr.postcode_risk as risk_score
        FROM postcode_distances pd
        JOIN postcode_risk pr ON pd.secondary_postcode = pr.postcode
        WHERE pd.primary_postcode = :postcode
        ORDER BY pd.distance_meters ASC
        LIMIT 20
    """, {"postcode": postcode})

    for postcode_data in nearest_postcodes:
        try:
            parking_data = db.get_parking_by_postcode(postcode_data['postcode'])
            postcode_data['parking_count'] = len(parking_data) if parking_data else 0
        except:
            postcode_data['parking_count'] = 0

    return nearest_postcodes

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
