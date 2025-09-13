from fastapi import APIRouter, Query, Request
from fastapi.responses import PlainTextResponse

router = APIRouter()


@router.get("/v1/search")
def search(request: Request, q: str = Query(..., description="Search query for suburb or postcode")):
    db = request.app.state.db
    rows = db.fetch_all("""
        SELECT locality as suburb, postcode, local_government_area as lga, postcode_risk as risk_score
        FROM postcode_risk
        WHERE locality LIKE '%' || :q || '%' OR postcode LIKE '%' || :q || '%'
        LIMIT 20
    """, {"q": q})
    return [{"label": f"{r['suburb']}, {r['postcode']}", **r} for r in rows]

