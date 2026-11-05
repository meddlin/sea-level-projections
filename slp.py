import csv
from dataclasses import dataclass
from typing import Dict, List, Optional

YEARS = (2005, 2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100, 2110, 2120, 2130, 2140, 2150)


def _to_float(value: Optional[str]) -> Optional[float]:
  """Blank or non-numeric cells become None instead of raising."""
  try:
    return float(value)
  except (TypeError, ValueError):
    return None


@dataclass
class Projection:
  psmsl_site: str
  psmsl_id: str
  noaa_id: str
  noaa_name: str
  rsl_grid_num: str
  lat: Optional[float]
  long: Optional[float]
  rsl: Dict[int, Optional[float]]  # year -> relative sea level (cm); None if the cell was blank

  @classmethod
  def from_row(cls, row: Dict[str, str]) -> "Projection":
    return cls(
      psmsl_site=row['PSMSL Site'],
      psmsl_id=row['PSMSL ID'],
      noaa_id=row['NOAA ID'],
      noaa_name=row['NOAA Name'],
      rsl_grid_num=row['RSL GridNum'],
      lat=_to_float(row['Lat']),
      long=_to_float(row['Long']),
      rsl={year: _to_float(row[f'RSL{year} (cm)']) for year in YEARS},
    )


def load_projections(path: str) -> List[Projection]:
  with open(path, newline='') as file:
    return [Projection.from_row(row) for row in csv.DictReader(file)]
