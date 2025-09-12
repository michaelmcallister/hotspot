from fastapi import FastAPI
from routes import health

app = FastAPI(title="Hotspot API", version="0.0.1")

app.include_router(health.router)

