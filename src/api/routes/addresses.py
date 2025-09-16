from fastapi import APIRouter, Path, Query, Request
from typing import Optional

router = APIRouter()

@router.get("/v1/addresses/{postcode}")
def get_addresses(
    request: Request,
    postcode: str = Path(..., description="Postcode to filter addresses"),
    q: Optional[str] = Query(None, description="Search query for address")
):
    db = request.app.state.db

    if q:
        rows = db.fetch_all("""
            SELECT address, suburb, postcode
            FROM victorian_addresses
            WHERE postcode = :postcode
              AND LOWER(address) LIKE '%' || LOWER(:query) || '%'
            ORDER BY address
            LIMIT 20
        """, {"postcode": postcode, "query": q})
    else:
        rows = db.fetch_all("""
            SELECT address, suburb, postcode
            FROM victorian_addresses
            WHERE postcode = :postcode
            ORDER BY address
            LIMIT 20
        """, {"postcode": postcode})

    return rows
