import argparse
import sys
from pathlib import Path

from plotting import save_graph
from slp import load_projections


def main() -> int:
  parser = argparse.ArgumentParser(description='Chart NOAA sea level projections, one image per row.')
  parser.add_argument('csv', nargs='?', default='slp_data.csv', help='projection CSV (default: slp_data.csv)')
  parser.add_argument('--out', default='output', help='directory for chart images (default: output)')
  parser.add_argument('--limit', type=int, help='only chart the first N rows')
  args = parser.parse_args()

  try:
    projections = load_projections(args.csv)
  except FileNotFoundError:
    print(f'CSV not found: {args.csv} (see README for where to get it)', file=sys.stderr)
    return 1

  for index, projection in enumerate(projections[:args.limit]):
    print(f'{save_graph(projection, index, Path(args.out))} ...saved')
  return 0


if __name__ == '__main__':
  sys.exit(main())
