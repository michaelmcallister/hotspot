from fastapi import APIRouter, Query, Request
from fastapi.responses import PlainTextResponse

router = APIRouter()

@router.get("/v1/risk/compare")
def risk_compare(request: Request, postcode: str = Query(...)):
    db = request.app.state.db
    base = db.fetch_all("""
        SELECT postcode, locality AS suburb, local_government_area AS lga,
               motorcycle_theft_rate, postcode_risk AS risk_score
        FROM postcode_risk WHERE postcode = :pc LIMIT 1
    """, {"pc": postcode})
    if not base:
        raise HTTPException(status_code=404, detail="Postcode not found")
    defaults = db.fetch_all("SELECT * FROM default_risk LIMIT 1")
    return {"base": base[0], "defaults": (defaults[0] if defaults else None)}

