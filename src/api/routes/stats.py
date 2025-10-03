from fastapi import APIRouter, Query, Request
from fastapi.responses import PlainTextResponse

router = APIRouter()

@router.get("/v1/risk/top")
def risk_top(request: Request, scope: str = "postcode", order: str = "desc", limit: int = Query(20, ge=1, le=200)):
    db = request.app.state.db
    if scope == "postcode":
        return db.fetch_all(f"""
            SELECT postcode, locality AS suburb, local_government_area AS lga,
                   postcode_risk AS risk_score
            FROM postcode_risk
            ORDER BY risk_score {"DESC" if order=="desc" else "ASC"}
            LIMIT :limit
        """, {"limit": limit})
    if scope == "lga":
        return db.fetch_all(f"""
            SELECT local_government_area AS lga,
                   ROUND(AVG(postcode_risk),6) AS avg_risk,
                   COUNT(*) AS postcode_count
            FROM postcode_risk
            GROUP BY local_government_area
            ORDER BY avg_risk {"DESC" if order=="desc" else "ASC"}
            LIMIT :limit
        """, {"limit": limit})
    raise HTTPException(status_code=400, detail="scope must be postcode or lga")

@router.get("/v1/stats/summary")
def stats_summary(request: Request):
    db = request.app.state.db
    return db.fetch_all("""
        SELECT
          (SELECT COUNT(*) FROM postcode_risk) AS total_postcodes,
          (SELECT COUNT(DISTINCT local_government_area) FROM postcode_risk) AS total_lgas,
          (SELECT ROUND(AVG(postcode_risk),6) FROM postcode_risk) AS avg_postcode_risk,
          (SELECT COUNT(*) FROM model_risk) AS total_models
    """)[0]
