"""Tayari FastAPI application entrypoint."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

app = FastAPI(
    title="Tayari — Anticipatory Action Co-pilot",
    description="Operational reasoning layer between ICPAC forecasts and last-mile action.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict:
    return {
        "name": "Tayari",
        "tagline": "From ICPAC forecast to last-mile action.",
        "docs": "/docs",
    }


# Routers are registered here as they are implemented.
from app.api.routes import health, ibf, messages  # noqa: E402

app.include_router(health.router)
app.include_router(ibf.router)
app.include_router(messages.router)
