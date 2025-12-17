# 🌊 Charting the Currents — 20-Year Spatio-Temporal Hotspot Analysis of Squid Catch

## 🌍 Real-World Value
This project aggregates 20 years of squid catch data into spatial hotspots, helping fisheries managers, policymakers, and research teams identify persistent and emerging high-catch areas. It enables evidence-based planning for marine resource management and enforcement of territorial fishing laws.

**Who This Helps**
- Fisheries agencies: identify high-density fishing areas for management and regulation
- Research labs: explore spatio-temporal patterns in cephalopod fisheries
- NGOs & policy groups: prioritize monitoring and conservation efforts

**Why It Matters**
Traditional CPUE (Catch Per Unit Effort) metrics can be noisy and influenced by gear, vessel, and environmental variability. Mapping catch density over time reveals consistent hotspots and informs ecosystem-based management decisions.

---

## 📘 Executive Summary
**What we did:** Aggregated vessel-based catch data into spatial grids, calculated yearly CPUE, and visualized 20 years of squid fishing hotspots.  
**Main outcomes:**
- Hotspots shift geographically over time, reflecting ecological and regulatory patterns
- Peak catches concentrated in specific regions, especially during 2010–2011
- By 2020, fishing activity aligned with EEZ regulations
**Why it matters:** The maps and CPUE trends highlight both ecological patterns and management impacts over two decades.

**Data scope:** 20-year dataset of vessel fishing events with spatial coordinates, environmental variables (SST, Chlorophyll-a), and catch volumes.

---

## 🧱 Database schema and analysis workflow

The diagram below shows the database tables used in the GIS analysis and
the flow of data from raw CSV ingestion to spatial aggregation.<br><br>
![Database schema](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/projectA_hotspots/tables/pA_ERD.drawio.png)

---

## 🧩 Module Overview
**Core Objectives**
- Aggregate catch into 0.25° spatial grids
- Identify annual hotspots based on CPUE
- Export GeoJSON, GeoPackage, PNGs, and summary tables for analysis and dashboard integration

**Outputs Generated**
- `spatial/grid_025deg.geojson` — 0.25° reference grid
- `spatial/hotspots_yearly.geojson` — yearly hotspot points
- `spatial/hotspots_aggregated.gpkg` — combined layers for visualization
- `spatial/qgis_project.qgz` — QGIS project file with styling
- `outputs/maps/` — PNG snapshots of key years (2000, 2010, 2011, 2020)
- `outputs/tables/hotspot_summary.csv` — yearly catch summary with CPUE

---

## 🔧 Tools & Techniques

**Core Stack**
- **PostgreSQL + PostGIS:** spatial database, queries, and aggregation
- **QGIS:** visualization, layer styling, and GeoPackage exports
- **Python / Jupyter Notebooks:** exploratory analysis, temporal animations, and plotting

**Key Methods**
- Spatial join and aggregation into grid cells
- Yearly CPUE calculation
- Heatmap visualization of hotspots
- Export of canonical spatial outputs for dashboards
- Log-scaled graduated symbology applied at the visualization stage to represent highly skewed catch distributions while preserving raw values for analysis


---

## 🗄️ Database Configuration (Required)

This project connects to a PostgreSQL/PostGIS database using **environment variables**.  
Database credentials are **not stored in the repository** for security reasons.

### Required Environment Variables
The following variables must be defined on your local machine before running the notebooks:

- `PGUSER` — PostgreSQL username  
- `PGPASSWORD` — PostgreSQL password  
- `PGHOST` — database host (e.g. `localhost`)  
- `PGPORT` — database port (default: `5432`)  
- `PGDATABASE` — database name  

### Example (macOS / Linux / Git Bash)

macOS/Linux(bash)
```bash
export PGUSER=postgres
export PGPASSWORD=your_password
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=your_database
```

Windows Notes

- If using Git Bash, environment variables only exist in that shell session.

 - If Jupyter is launched from Anaconda Navigator or VS Code, those variables may not be visible.

 - In that case, variables can be set inside Python for the session

   ```
    import os
    os.environ["PGUSER"] = "postgres"
    os.environ["PGPASSWORD"] = "your_password"
    os.environ["PGHOST"] = "localhost"
    os.environ["PGPORT"] = "5432"
    os.environ["PGDATABASE"] = "your_database"
    ```

Security Notes

 - Do not commit credentials directly into notebooks or scripts

 - .env files (if used) should be added to .gitignore

 - Each user must configure their own local database credential
   
---

## 📈 Visual Outputs
> Go to "📸 Static Previews" section below for a quick preview of outputs.
> 
| Visualization | Description | File Location |
|---------------|------------|---------------|
| Hotspot Map 2000 | Catch density for 2000 | `outputs/maps/hotspot_2000.png` |
| Hotspot Map 2010 | Shifted catch hotspot | `outputs/maps/hotspot_2010.png` |
| Hotspot Map 2011 | Major geographic shift | `outputs/maps/hotspot_2011.png` |
| Hotspot Map 2020 | Post-EEZ enforcement | `outputs/maps/hotspot_2020.png` |
| Animated  Hotspots | Spatio-temporal evolution | `outputs/maps/animated_hotspots.gif`|
| Yearly Summary Table | Total catch, effort, CPUE | `outputs/tables/hotspot_summary.csv` |

Note on Map Symbology  
Catch quantities displayed in the hotspot maps use logarithmic (base-10) graduated color scaling in QGIS. This transformation is applied only at the visualization stage to improve interpretability of highly right-skewed fisheries data and to emphasize relative hotspot intensity. All analytical calculations (e.g., CPUE, summaries, and trend analysis) are performed using raw catch values in kilograms.

---

## 📉 Limitations & Future Work
- Hotspots are based on available vessel data; unreported catches are not included
- Grid size (0.25°) may smooth fine-scale patterns; future work could experiment with smaller grids
- Environmental drivers (SST, Chlorophyll-a, depth) not yet incorporated into predictive models — next step for integration into Streamlit/Shiny dashboard
- Future work could compare log-scaled visual hotspot patterns with alternative normalizations (e.g., effort-normalized density surfaces) to assess sensitivity of hotspot delineation.


---

## 🧭 Summary Statement
This module establishes a **robust, industry-standard workflow** for spatio-temporal hotspot analysis of squid catch. Outputs are suitable for visual exploration, reporting, and integration into interactive dashboards, providing both ecological insight and regulatory intelligence.

---

## 🤝 Collaboration & Contact
Contributions and extensions are welcome, particularly in:
- Cephalopod ecology and fishery stock assessment
- Spatio-temporal modeling and visualization
- Interactive dashboard development (Streamlit/Shiny)

📬 [Email](mailto:euchiejnpierre@gmail.com) | [LinkedIn](https://www.linkedin.com/in/euchiejnpierre/)

---

## 🔒 Data Confidentiality Notice
This dataset is a simulated approximation of a real-world squid stock assessment
dataset used during my tenure as a part-time research assistant at National Taiwan
University. Although it closely resembles actual data, any interpretation or
conclusions drawn here cannot be assumed to represent real conditions in the
region.

---

## 📸 Static Previews

**Hotspot Map - 2000 (Baseline)**
- ![Hotspot Map — 2000](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/projectA_hotspots/maps/hotspots_2000.png)

**Hotspot Map - 2010 (Shifted Catch Hotspots)**
- ![Hotspot Map — 2010](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/projectA_hotspots/maps/hotspots_2010.png)

**Hotspot Map - 2011 (Major Geographic Shift)**
- ![Hotspot Map — 2011](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/projectA_hotspots/maps/hotspots_2011.png)

**Hotspot Map - 2020 (Post EEZ Enforcement)**
- ![Hotspot Map — 2020](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/projectA_hotspots/maps/hotspots_2020.png)

**Animated Hotspot Shift - 2000, 2010, 2011, 2020**
- ![Animated Hotspot Shifts](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/projectA_hotspots/animated_hotspots.gif)

**CPUE Time Series**
- ![Catch & CPUE Time Series](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/projectA_hotspots/plots/squid_catch_cpue_over_time.png)

---

> 📁 For more on spatio-temporal mapping, spatial database design, and geospatial
visual analytics using PostGIS and QGIS, see the other modules in the
GeoTentacles repository.
> 
