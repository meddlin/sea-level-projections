# Sea Level Rise Projections

## Getting Started

### Web app (Docker)

Requires Docker. Put the NOAA CSV at `data/slp_data.csv` (see [Data Source](#data-source)), then:

```bash
docker compose up --build
```

- Dashboard: http://localhost:8000
- JupyterLab (also embedded under the dashboard's *Notebook* tab): http://localhost:8888

JupyterLab is protected by a token (default `sealevel`; set `JUPYTER_TOKEN` in a `.env` file to change it).
The dashboard hands that token to the embedded page, so treat both ports as open to anyone on your
network. This is meant for a trusted home network only; do not expose it to the internet.

Notebooks live in `notebooks/` and are saved there from JupyterLab (start with `notebooks/analysis.ipynb`).

### Command line

1. Download the projection CSV and save it in the repo root as `slp_data.csv`. CSV files are gitignored.
2. Install dependencies: `pip install -r requirements.txt`
3. Generate the charts: `python main.py` (one PNG per row, written to `output/`).
   - `python main.py path/to/file.csv --out charts --limit 10` to change the input, output folder, or chart only the first rows.

## Data Source

**Want the CSV data?** 👇

2022 Sea Level Rise Technical Report Data Files

[https://oceanservice.noaa.gov/hazards/sealevelrise/sealevelrise-data.html](https://oceanservice.noaa.gov/hazards/sealevelrise/sealevelrise-data.html)

**Want to read the full PDF report?** 👇

Technical Report - 2022 Sea Level Rise

[https://oceanservice.noaa.gov/hazards/sealevelrise/sealevelrise-tech-report-sections.html](https://oceanservice.noaa.gov/hazards/sealevelrise/sealevelrise-tech-report-sections.html)