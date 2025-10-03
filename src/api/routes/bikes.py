from fastapi import APIRouter, Query, Request, HTTPException, Path
from fastapi.responses import PlainTextResponse
from typing import List, Dict, Any
from models import MotorcycleModel

router = APIRouter(tags=["Motorcycles"])

@router.get(
    "/v1/models",
    summary="List motorcycle models",
    description="Search and filter motorcycle models with theft risk data",
    response_description="List of motorcycle models with risk scores",
    response_model=List[MotorcycleModel]
)
def list_models(
    request: Request,
    brand: str | None = Query(None, description="Filter by brand name"),
    model: str | None = Query(None, description="Filter by model name"),
    min_total: int = Query(0, ge=0, description="Minimum total theft count"),
    sort: str = Query("risk_desc", description="Sort order", pattern="^(risk_desc|risk_asc|total_desc|total_asc|brand|model)$"),
    limit: int = Query(100, ge=1, le=500, description="Maximum results to return"),
    offset: int = Query(0, ge=0, description="Number of results to skip"),
) -> List[MotorcycleModel]:
    db = request.app.state.db
    clauses, params = ["total >= :min_total"], {"min_total": min_total}
    if brand: clauses.append("brand LIKE '%' || :brand || '%'"); params["brand"]=brand.lower()
    if model: clauses.append("model LIKE '%' || :model || '%'"); params["model"]=model.lower()
    where_sql = "WHERE " + " AND ".join(clauses)
    sort_sql = {"risk_desc":"model_risk DESC","risk_asc":"model_risk ASC","total_desc":"total DESC","total_asc":"total ASC","brand":"brand ASC","model":"model ASC"}.get(sort,"model_risk DESC")
    results = db.fetch_all(f"""
        SELECT brand, model, total, percentage, model_risk
        FROM model_risk
        {where_sql}
        ORDER BY {sort_sql}
        LIMIT :limit OFFSET :offset
    """, {**params, "limit": limit, "offset": offset})
    return [MotorcycleModel(**result) for result in results]

@router.get(
    "/v1/models/{brand}/{model}",
    summary="Get motorcycle details",
    description="Get detailed theft risk data for a specific motorcycle model",
    response_description="Motorcycle model with complete theft statistics",
    response_model=MotorcycleModel
)
def model_detail(
    request: Request,
    brand: str = Path(..., description="Motorcycle brand name"),
    model: str = Path(..., description="Motorcycle model name")
) -> MotorcycleModel:
    db = request.app.state.db
    row = db.fetch_all("""
        SELECT brand, model, total, percentage, model_risk
        FROM model_risk
        WHERE brand = :b AND model = :m
        LIMIT 1
    """, {"b": brand.lower(), "m": model.lower()})
    if not row:
        raise HTTPException(status_code=404, detail="Model not found")
    return MotorcycleModel(**row[0])

