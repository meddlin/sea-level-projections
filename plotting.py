import re
from pathlib import Path

from matplotlib.figure import Figure

from slp import Projection


def _slug(text: str) -> str:
  return re.sub(r'[^A-Za-z0-9]+', '_', text).strip('_') or 'unnamed'


def draw_graph(projection: Projection) -> Figure:
  """Bar chart of projected relative sea level, one bar per available year."""
  points = [(year, cm) for year, cm in projection.rsl.items() if cm is not None]

  # Figure (not pyplot) keeps no global state, so nothing leaks across hundreds of charts.
  fig = Figure()
  ax = fig.subplots()
  ax.bar([str(year) for year, _ in points], [cm for _, cm in points], width=1, edgecolor='white', linewidth=1.5)
  ax.set_title(projection.noaa_name)
  ax.set_xlabel('year')
  ax.set_ylabel('projected (cm)')
  ax.tick_params(axis='x', labelrotation=45)
  return fig


def save_graph(projection: Projection, index: int, out_dir: Path) -> Path:
  """Save one chart; the row index keeps filenames unique when a site name repeats."""
  out_dir.mkdir(parents=True, exist_ok=True)
  path = out_dir / f'{index:04d}_{_slug(projection.noaa_name)}.png'
  draw_graph(projection).savefig(path, bbox_inches='tight', dpi=200)
  return path
