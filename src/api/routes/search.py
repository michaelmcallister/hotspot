from fastapi import APIRouter, Query, Request
from fastapi.responses import PlainTextResponse
from typing import List
from models import SuburbSearchResult

router = APIRouter(tags=["Search"])

@router.get(
    "/v1/search",
    summary="Search suburbs",
    description="Search for Victorian suburbs by name or postcode with risk scoring",
    response_description="List of matching suburbs with risk scores",
    response_model=List[SuburbSearchResult]
)
def search(request: Request, q: str = Query(..., description="Search term (suburb name or postcode)", min_length=1)) -> List[SuburbSearchResult]:
    db = request.app.state.db
    rows = db.fetch_all("""
        SELECT locality as suburb, postcode, local_government_area as lga, postcode_risk as risk_score
        FROM postcode_risk
        WHERE locality LIKE '%' || :q || '%' OR postcode LIKE '%' || :q || '%'
        LIMIT 20
    """, {"q": q})
    return [SuburbSearchResult(label=f"{r['suburb']}, {r['postcode']}", **r) for r in rows]

