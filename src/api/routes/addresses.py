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
    return db.get_addresses_by_postcode(postcode, q)
