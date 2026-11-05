# Sea Level Rise Projections

## Getting Started

1. Download the projection CSV (see [Data Source](#data-source)) and save it in the repo root as `slp_data.csv`. CSV files are gitignored.
2. Install dependencies: `pip install -r requirements.txt`
3. Generate the charts: `python main.py` (one PNG per row, written to `output/`).
   - `python main.py path/to/file.csv --out charts --limit 10` to change the input, output folder, or chart only the first rows.
4. Or explore interactively in `analysis.ipynb`.

## Data Source

**Want the CSV data?** 👇

2022 Sea Level Rise Technical Report Data Files

[https://oceanservice.noaa.gov/hazards/sealevelrise/sealevelrise-data.html](https://oceanservice.noaa.gov/hazards/sealevelrise/sealevelrise-data.html)

**Want to read the full PDF report?** 👇

Technical Report - 2022 Sea Level Rise

[https://oceanservice.noaa.gov/hazards/sealevelrise/sealevelrise-tech-report-sections.html](https://oceanservice.noaa.gov/hazards/sealevelrise/sealevelrise-tech-report-sections.html)