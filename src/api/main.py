import argparse
import os
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from db_interface import get_database
from routes import health, search, bikes, lgas, risk, stats, addresses, parking, contact, postcodes


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

uvicorn_logger = logging.getLogger("uvicorn")
uvicorn_logger.handlers = []
uvicorn_logger.addHandler(logging.StreamHandler(sys.stdout))

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Hotspot API Server")
parser.add_argument(
    "--db",
    type=str,
    default="../data/hotspot.db",
    help="Path to SQLite database file (default: ../data/hotspot.db)"
)
parser.add_argument(
    "--static",
    type=str,
    default="../web/dist",
    help="Path to static files directory (default: ../web/dist)"
)
args, unknown = parser.parse_known_args()

# Get the appropriate database implementation
db = get_database()
env = os.environ.get('ENVIRONMENT', 'development')

static_path = Path(args.static).resolve()

@asynccontextmanager
async def lifespan(app: FastAPI):
    if env == 'production':
        logger.info(f"Connected to DynamoDB in {os.environ.get('AWS_DEFAULT_REGION', 'ap-southeast-2')} region")
        logger.info(f"Using table: {os.environ.get('DYNAMODB_TABLE', 'user_contributions')}")
    else:
        logger.info(f"Connected to SQLite database: {os.environ.get('SQLITE_DB_PATH')}")
    if static_path.exists():
        logger.info(f"Serving static files from: {static_path}")
    yield
    logger.info("Shutting down...")


app = FastAPI(title="Hotspot API", version="0.0.1", lifespan=lifespan)
app.state.db = db

app.include_router(health.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(lgas.router, prefix="/api")
app.include_router(risk.router, prefix="/api")
app.include_router(stats.router, prefix="/api")
app.include_router(bikes.router, prefix="/api")
app.include_router(addresses.router, prefix="/api")
app.include_router(parking.router, prefix="/api")
app.include_router(contact.router, prefix="/api")
app.include_router(postcodes.router, prefix="/api")

if static_path.exists():
    @app.get("/")
    async def read_index():
        return FileResponse(static_path / "index.html")

    if (static_path / "assets").exists():
        app.mount("/assets", StaticFiles(directory=static_path / "assets"), name="assets")

    # Catch-all route for Vue Router (client-side routing)
    # This must be defined last to avoid catching API routes
    @app.get("/{full_path:path}")
    async def catch_all(full_path: str):
        # Don't catch API routes
        if full_path.startswith("api/"):
            return {"detail": "Not found"}
        # Check if the path is a static file
        file_path = static_path / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        # Serve index.html for all other routes, Vue should handle this
        return FileResponse(static_path / "index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
