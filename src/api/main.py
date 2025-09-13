import argparse
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from database import Database
from routes import health, search


parser = argparse.ArgumentParser(description="Hotspot API Server")
parser.add_argument(
    "--db",
    type=str,
    default="../data/hotspot.db",
    help="Path to SQLite database file (default: ../data/hotspot.db)"
)
args, unknown = parser.parse_known_args()

db_path = Path(args.db).resolve()
if not db_path.exists():
    raise FileNotFoundError(f"Database file not found: {db_path}")

db = Database(str(db_path))

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Connected to database: {db_path}")
    yield
    print("Shutting down...")


app = FastAPI(title="Hotspot API", version="0.0.1", lifespan=lifespan)
app.state.db = db

app.include_router(health.router)
app.include_router(search.router)
