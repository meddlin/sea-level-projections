import os
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app import data

STATIC = Path(__file__).parent / "static"

app = FastAPI(title="Sea Level Projections")


@app.exception_handler(data.DataMissing)
def data_missing(request, exc):
    from fastapi.responses import JSONResponse

    return JSONResponse({"detail": f"Projection data not found ({exc}). Put slp_data.csv in the data/ folder."}, status_code=503)


@app.get("/api/config")
def config():
    return {
        "jupyter_port": int(os.environ.get("JUPYTER_PORT", "8888")),
        "jupyter_token": os.environ.get("JUPYTER_TOKEN", ""),
    }


@app.get("/api/meta")
def meta():
    return {
        "years": data.YEARS,
        "scenarios": data.SCENARIOS,
        "levels": data.LEVELS,
        "stations": data.stations(),
    }


@app.get("/api/projections/{site}")
def projections(site: str):
    result = data.site_projections(site)
    if not result:
        raise HTTPException(404, f"Unknown site: {site}")
    return result


@app.get("/api/ranking")
def ranking(year: int = 2100, scenario: str = "1.0", level: str = "MED"):
    if year not in data.YEARS or scenario not in data.SCENARIOS or level not in data.LEVELS:
        raise HTTPException(400, "Invalid year, scenario or level")
    return data.table(year, scenario, level)


app.mount("/static", StaticFiles(directory=STATIC), name="static")


@app.get("/")
def index():
    return FileResponse(STATIC / "index.html")
