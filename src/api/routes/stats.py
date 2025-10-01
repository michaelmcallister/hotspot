import logging
import time
from fastapi import APIRouter, Query, Request, HTTPException
from typing import Dict, Any, Optional
from models import StatisticsSummary, PaginatedRiskResponse

router = APIRouter(tags=["Statistics"])
logger = logging.getLogger(__name__)

_stats_cache: Optional[Dict[str, Any]] = None
_cache_timestamp: float = 0
CACHE_TTL_SECONDS = 300  # 5 minutes

@router.get(
    "/v1/statistics/summary",
    summary="Get platform statistics",
    description="Returns aggregated platform-wide statistics including coverage and submission counts",
    response_description="Summary statistics with caching for performance",
    response_model=StatisticsSummary
)
def get_statistics_summary(request: Request) -> StatisticsSummary:
    global _stats_cache, _cache_timestamp

    current_time = time.time()
    if _stats_cache and (current_time - _cache_timestamp) < CACHE_TTL_SECONDS:
        logger.info(f"Returning cached statistics (age: {int(current_time - _cache_timestamp)}s)")
        return StatisticsSummary(**_stats_cache)

    db = request.app.state.db

    total_postcodes = db.fetch_all("""
        SELECT COUNT(DISTINCT postcode) as count
        FROM postcode_risk
    """)[0]['count']

    try:
        total_addresses = db.fetch_all("""
            SELECT COUNT(*) as count
            FROM victorian_addresses
        """)[0]['count']
    except Exception as e:
        logger.warning(f"Could not fetch address count: {e}")
        total_addresses = 0

    total_lgas = db.fetch_all("""
        SELECT COUNT(DISTINCT local_government_area) as count
        FROM postcode_risk
    """)[0]['count']

    try:
        total_submissions = db.get_parking_submissions_count()
    except Exception as e:
        logger.error(f"Error fetching submission count: {e}")
        total_submissions = 0

    result = {
        "total_postcodes": total_postcodes,
        "total_addresses": total_addresses,
        "total_lgas": total_lgas,
        "total_submissions": total_submissions
    }

    _stats_cache = result
    _cache_timestamp = time.time()
    logger.info(f"Statistics cached at {_cache_timestamp}")

    return StatisticsSummary(**result)

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

@router.get(
    "/v1/risk/top",
    summary="Get risk rankings",
    description="Paginated list of suburbs or LGAs ranked by safety scores with search and sorting",
    response_description="Paginated risk data with total count",
    response_model=PaginatedRiskResponse
)
def risk_top(
    request: Request,
    scope: str = Query("postcode", description="Group by postcode or lga", pattern="^(postcode|lga)$"),
    page: int = Query(1, ge=1, description="Page number"),
    itemsPerPage: int = Query(20, ge=1, le=100, description="Results per page"),
    sortBy: str = Query(None, description="Column to sort by"),
    sortOrder: str = Query("desc", description="Sort direction", pattern="^(asc|desc)$"),
    search: str = Query(None, description="Search filter text")
) -> PaginatedRiskResponse:
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

    return PaginatedRiskResponse(items=items, total=total)
