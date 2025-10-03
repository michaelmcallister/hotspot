from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(tags=["Health"])

@router.get(
    "/health",
    response_class=PlainTextResponse,
    summary="Health check",
    description="Simple health check endpoint for monitoring",
    response_description="Returns 'ok' when service is running"
)
def health() -> str:
    return "ok"
