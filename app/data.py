"""Loads the NOAA 2022 sea level rise projections CSV and answers queries over it."""
import os
from functools import lru_cache
from pathlib import Path

import pandas as pd

DATA_FILE = Path(os.environ.get("DATA_DIR", "data")) / "slp_data.csv"

YEARS = [2005, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100, 2110, 2120, 2130, 2140, 2150]
YEAR_COLS = [f"RSL{y} (cm)" for y in YEARS]

# NOAA's five scenarios, named for the approximate global rise (m) by 2100.
SCENARIOS = {
    "0.3": "Low",
    "0.5": "Intermediate-Low",
    "1.0": "Intermediate",
    "1.5": "Intermediate-High",
    "2.0": "High",
}
LEVELS = ["LOW", "MED", "HIGH"]


class DataMissing(Exception):
    pass


@lru_cache(maxsize=1)
def load() -> pd.DataFrame:
    if not DATA_FILE.exists():
        raise DataMissing(f"{DATA_FILE} not found")
    df = pd.read_csv(DATA_FILE)
    df[["scenario", "level"]] = df["Scenario"].str.split(" - ", expand=True)
    df["NOAA Name"] = df["NOAA Name"].fillna("")
    # Rows without a NOAA name are interpolated grid cells; the dashboard uses named stations.
    return df[df["NOAA Name"] != ""].copy()


def stations() -> list[dict]:
    df = load()
    first = df.drop_duplicates("NOAA Name")
    return [
        {
            "name": r["NOAA Name"],
            "noaa_id": str(int(r["NOAA ID"])),
            "region": r["Regional Classification"] if isinstance(r["Regional Classification"], str) else "Global",
            "lat": None if pd.isna(r["Lat"]) else float(r["Lat"]),
            "lon": None if pd.isna(r["Long"]) else float(r["Long"]),
            "vlm": float(r["RSL contribution from VLM (trend: cm/year)"]),
        }
        for _, r in first.iterrows()
    ]


def site_projections(name: str) -> dict:
    df = load()
    sub = df[df["NOAA Name"] == name]
    out: dict = {}
    for _, r in sub.iterrows():
        out.setdefault(r["scenario"], {})[r["level"]] = [int(r[c]) for c in YEAR_COLS]
    return out


def table(year: int, scenario: str, level: str) -> list[dict]:
    df = load()
    col = f"RSL{year} (cm)"
    sub = df[(df["scenario"] == scenario) & (df["level"] == level) & (df["NOAA Name"] != "GMSL")]
    return sorted(
        ({"name": r["NOAA Name"], "region": r["Regional Classification"], "value": int(r[col])} for _, r in sub.iterrows()),
        key=lambda x: -x["value"],
    )
