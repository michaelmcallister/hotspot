from fastapi import APIRouter, Query, Request, HTTPException

router = APIRouter()

SCOPE_CONFIG = {
    "postcode": {
        "sort_columns": {
            "postcode": "postcode",
            "suburb": "locality",
            "lga": "local_government_area",
            "safety_score": "postcode_risk"
        },
        "default_sort": "postcode_risk",
        "search_columns": ["postcode", "locality", "local_government_area"],
        "select": "SELECT postcode, locality AS suburb, local_government_area AS lga, postcode_risk AS risk_score FROM postcode_risk",
        "count": "SELECT COUNT(*) as count FROM postcode_risk",
        "group_by": None
    },
    "lga": {
        "sort_columns": {
            "lga": "local_government_area",
            "postcode_count": "postcode_count",
            "avg_safety": "avg_risk"
        },
        "default_sort": "avg_risk",
        "search_columns": ["local_government_area"],
        "select": "SELECT local_government_area AS lga, ROUND(AVG(postcode_risk),6) AS avg_risk, COUNT(*) AS postcode_count FROM postcode_risk",
        "count": "SELECT COUNT(DISTINCT local_government_area) as count FROM postcode_risk",
        "group_by": "GROUP BY local_government_area"
    }
}

@router.get("/v1/risk/top")
def risk_top(
    request: Request,
    scope: str = "postcode",
    page: int = Query(1, ge=1),
    itemsPerPage: int = Query(20, ge=1, le=100),
    sortBy: str = Query(None),
    sortOrder: str = Query("desc"),
    search: str = Query(None)
):
    if scope not in SCOPE_CONFIG:
        raise HTTPException(status_code=400, detail="scope must be postcode or lga")

    config = SCOPE_CONFIG[scope]
    db = request.app.state.db

    offset = (page - 1) * itemsPerPage
    params = {"limit": itemsPerPage, "offset": offset}

    filter_clause = ""
    if search:
        search_conditions = " OR ".join([f"{col} LIKE :search" for col in config["search_columns"]])
        filter_clause = f"WHERE {search_conditions}" if not config["group_by"] else f"HAVING {search_conditions}"
        params["search"] = f"%{search}%"

    sort_column = config["sort_columns"].get(sortBy, config["default_sort"])
    sort_direction = "DESC" if sortOrder == "desc" else "ASC"

    count_filter = filter_clause if not config["group_by"] else filter_clause.replace("HAVING", "WHERE")
    count_query = f"{config['count']} {count_filter}"
    total = db.fetch_all(count_query, params)[0]['count']

    group_clause = f"{config['group_by']}" if config["group_by"] else ""
    data_query = f"""
        {config['select']}
        {group_clause}
        {filter_clause}
        ORDER BY {sort_column} {sort_direction}
        LIMIT :limit OFFSET :offset
    """
    items = db.fetch_all(data_query, params)

    return {"items": items, "total": total}
