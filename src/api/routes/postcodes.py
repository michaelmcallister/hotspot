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
            pd.distance_meters as distance_in_meters
        FROM postcode_distances pd
        JOIN postcode_risk pr ON pd.secondary_postcode = pr.postcode
        WHERE pd.primary_postcode = :postcode
        ORDER BY pd.distance_meters ASC
        LIMIT 20
    """, {"postcode": postcode})

    return nearest_postcodes
