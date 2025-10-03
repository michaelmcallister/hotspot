from fastapi import APIRouter, Query, Request
from fastapi.responses import PlainTextResponse

router = APIRouter()

@router.get("/v1/lgas")
def lga_rollups(request: Request, q: str | None = None, sort: str = Query("avg_desc")):
    db = request.app.state.db
    where = "WHERE local_government_area LIKE '%' || :q || '%'" if q else ""
    params = {"q": q} if q else {}
    sort_sql = {"avg_desc":"avg_risk DESC","avg_asc":"avg_risk ASC","count_desc":"postcode_count DESC","count_asc":"postcode_count ASC","lga":"lga ASC"}.get(sort,"avg_desc")
    return db.fetch_all(f"""
        SELECT local_government_area AS lga,
               COUNT(*) AS postcode_count,
               ROUND(AVG(postcode_risk), 6) AS avg_risk,
               MIN(postcode_risk) AS min_risk,
               MAX(postcode_risk) AS max_risk
        FROM postcode_risk
        {where}
        GROUP BY local_government_area
        ORDER BY {sort_sql}
    """, params)

@router.get("/v1/lgas/{lga}/postcodes")
def lga_postcodes(request: Request, lga: str, order: str = Query("desc", description="desc|asc")):
    db = request.app.state.db
    order_sql = "DESC" if order == "desc" else "ASC"
    rows = db.fetch_all(f"""
        SELECT postcode, locality AS suburb, long, lat,
               postcode_risk AS risk_score
        FROM postcode_risk
        WHERE local_government_area = :lga
        ORDER BY postcode_risk {order_sql}, postcode ASC
    """, {"lga": lga})
    if not rows:
        raise HTTPException(status_code=404, detail="LGA not found or empty")
    return rows

