from fastapi import APIRouter, Query, Request
from fastapi.responses import PlainTextResponse

router = APIRouter()

@router.get("/v1/models")
def list_models(
    request: Request,
    brand: str | None = None,
    model: str | None = None,
    min_total: int = Query(0, ge=0),
    sort: str = Query("risk_desc", description="risk_desc|risk_asc|total_desc|total_asc|brand|model"),
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
):
    db = request.app.state.db
    clauses, params = ["total >= :min_total"], {"min_total": min_total}
    if brand: clauses.append("brand LIKE '%' || :brand || '%'"); params["brand"]=brand.lower()
    if model: clauses.append("model LIKE '%' || :model || '%'"); params["model"]=model.lower()
    where_sql = "WHERE " + " AND ".join(clauses)
    sort_sql = {"risk_desc":"model_risk DESC","risk_asc":"model_risk ASC","total_desc":"total DESC","total_asc":"total ASC","brand":"brand ASC","model":"model ASC"}.get(sort,"model_risk DESC")
    return db.fetch_all(f"""
        SELECT brand, model, total, percentage, model_risk
        FROM model_risk
        {where_sql}
        ORDER BY {sort_sql}
        LIMIT :limit OFFSET :offset
    """, {**params, "limit": limit, "offset": offset})

@router.get("/v1/models/{brand}/{model}")
def model_detail(request: Request, brand: str, model: str):
    db = request.app.state.db
    row = db.fetch_all("""
        SELECT brand, model, total, percentage, model_risk
        FROM model_risk
        WHERE brand = :b AND model = :m
        LIMIT 1
    """, {"b": brand.lower(), "m": model.lower()})
    if not row:
        raise HTTPException(status_code=404, detail="Model not found")
    return row[0]

