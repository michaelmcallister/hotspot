from fastapi import APIRouter, Path, Query, Request
from typing import Optional, List
from models import Address

router = APIRouter(tags=["Addresses"])

@router.get(
    "/v1/postcode/{postcode}/addresses",
    summary="Get addresses by postcode",
    description="Retrieve validated Victorian addresses for a specific postcode with optional search filtering",
    response_description="List of matching addresses with full details",
    response_model=List[Address]
)
def get_addresses(
    request: Request,
    postcode: str = Path(..., description="Victorian postcode", pattern="^[0-9]{4}$"),
    q: Optional[str] = Query(None, description="Filter addresses by partial match")
) -> List[Address]:
    db = request.app.state.db
    results = db.get_addresses_by_postcode(postcode, q)
    return [Address(**addr) for addr in results]
