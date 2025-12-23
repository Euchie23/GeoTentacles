# 🌊 Charting the Currents — 20-Year Spatio-Temporal Hotspot Analysis of Squid Catch

## 📘 Executive Summary
**What we did:**
Aggregated vessel-based catch events into origin-aligned 0.25° polygon grid cells, calculated yearly CPUE per cell, and visualized 20 years of squid fishing hotspots.  
**Main outcomes:**
- Hotspots shift geographically over time, reflecting ecological and regulatory patterns
- Peak catches concentrated in specific regions, especially during 2010–2011
- By 2020, fishing activity aligned with EEZ regulations

**Data scope:** 20-year dataset of vessel fishing events with spatial coordinates, environmental variables (SST, Chlorophyll-a), and catch volumes.

---

## 🌍 Real-World Value
This project aggregates 20 years of squid catch data into polygon-based spatial grid cells (0.25° × 0.25°), enabling robust hotspot detection and comparison across time. It enables evidence-based planning for marine resource management and enforcement of territorial fishing laws.

**Who This Helps**
- Fisheries agencies: identify high-density fishing areas for management and regulation
- Research labs: explore spatio-temporal patterns in cephalopod fisheries
- NGOs & policy groups: prioritize monitoring and conservation efforts

**Why It Matters**
Traditional CPUE (Catch Per Unit Effort) metrics can be noisy and influenced by gear, vessel, and environmental variability. Mapping catch density over time reveals consistent hotspots and informs ecosystem-based management decisions.

---

## 🎯 Applied Use Case

This hotspot analysis is designed to support **spatially explicit fisheries decision-making** by revealing where squid fishing activity concentrates, how hotspots shift over time, and how management boundaries influence behavior.

### Example Applications

**1. Spatial Management & Enforcement**
Fisheries agencies can use yearly hotspot maps to:
- Identify consistently high-pressure fishing areas
- Allocate patrol and monitoring resources more efficiently
- Evaluate whether fishing effort shifts align with EEZ enforcement or regulatory changes

By comparing hotspot locations before and after regulatory milestones (e.g., post-2010 EEZ alignment), managers can assess compliance indirectly through spatial behavior.

**2. Ecosystem-Based Fisheries Management**
Hotspot persistence and movement provide insight into:
- Core habitat use by *Illex argentinus*
- Interannual shifts driven by environmental variability or stock dynamics
- Regions where fishing pressure repeatedly overlaps with key ecological zones

This supports ecosystem-based planning beyond single-year CPUE metrics.

**3. Research & Survey Design**
Research groups can use hotspot outputs to:
- Prioritize regions for scientific surveys or tagging campaigns
- Compare spatial CPUE patterns with environmental drivers (SST, Chlorophyll-a)
- Design stratified sampling frameworks based on historical fishing intensity

**4. NGO & Policy Analysis**
Conservation organizations and policy teams can:
- Communicate long-term spatial fishing patterns to stakeholders
- Identify areas of recurring pressure that may warrant protection or monitoring
- Use visual hotspot evidence in policy briefs and advocacy materials

⚠️ Interpretation Note: Hotspots indicate historical fishing activity density. Not direct biomass. Use alongside ecological and regulatory indicators.

---

## 🧱 Database schema and analysis workflow

The diagram below illustrates the database tables used in the GIS analysis and the flow of data from raw CSV ingestion to spatial aggregation. For a complete overview of all tables and columns, please see our [Data Dictionary](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/hotspot_dynamics/tables/Data_Dictionary.pdf).
Aggregation uses point-in-polygon spatial joins, calculating CPUE per 0.25° polygon annually. Outputs include GeoJSON, GeoPackage, and visual maps. This approach prevents visual overlap, supports area-based summaries, and aligns with industry-standard fisheries hotspot workflows.<br><br>
![Database schema](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/hotspot_dynamics/tables/pA_ERD.drawio.png)

---
spatial/grid_025deg_poly.geojson — 0.25° × 0.25° polygon reference grid
spatial/hotspots_yearly.geojson — yearly polygon-based hotspot layers

## 🧩 Module Overview
**Core Objectives**
- Aggregate catch into 0.25° × 0.25° polygon grid cells
- Identify annual hotspots based on CPUE
- Export GeoJSON, GeoPackage, PNGs, and summary tables for analysis and dashboard integration

**Outputs Generated**
- `spatial/grid_025deg_poly.geojson` — 0.25° × 0.25° polygon reference grid
- `spatial/hotspots_yearly.geojson` — yearly polygon-based hotspot layers
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
- Point-in-polygon spatial joins to aggregate fishing events into polygon grid cells
- Polygon-level CPUE calculated as total catch per vessel-day within each grid cell and year
- Yearly CPUE calculation
- Heatmap visualization of hotspots
- Export of canonical spatial outputs for dashboards 
- Log-scaled (base-10) graduated symbology applied at the visualization stage in QGIS to represent highly skewed catch and CPUE distributions while preserving raw values for analysis and web delivery via GeoJSON; logarithmic transformation is used solely to improve visual interpretability of highly skewed spatial patterns.


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
> Go to "📸 Static Previews" section below for a quick preview of main and supplementary outputs.
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
Legend values display back-transformed CPUE values (kg per vessel-day). While grid cells are symbolized using a log₁₀ transformation to handle extreme skewness, legend labels are shown in real-world units to ensure interpretability for non-technical audiences. Color differences therefore represent orders-of-magnitude changes in catch efficiency rather than linear increments.

---

## 📉 Limitations & Future Work
- Polygon grid size (0.25° × 0.25°) may smooth fine-scale fishing behavios; future work could experiment with smaller grids
- Environmental drivers (SST, Chlorophyll-a, depth) not yet incorporated into predictive models — next step for integration into Streamlit/Shiny dashboard
- Future work could compare log-scaled visual hotspot patterns with alternative normalizations (e.g., effort-normalized density surfaces) to assess sensitivity of hotspot delineation.


---

## 🧭 Summary Statement
This module establishes **a robust, polygon-based, industry-standard workflow** for spatio-temporal hotspot analysis of squid catch. Outputs are suitable for visual exploration, reporting, and integration into interactive dashboards, providing both ecological insight and regulatory intelligence.

---

## 🔗 Continuation: 🗺️ Forecasting the Swarms (Squid Catch Hotspot Predictions using Classification Modelling)

This hotspot analysis serves as the spatial foundation for **Forecasting the Swarms**, which extends the workflow into predictive modeling. 

Forecasting the Swarms focuses on:
- Predicting hotspot likelihood rather than historical density
- Quantifying uncertainty using probability surfaces
- Validating predictions across independent years

➡️ See [**Forecasting the Swarms — Squid Catch Hotspot Prediction (ML)**](https://github.com/Euchie23/GeoTentacles/blob/main/hotspot_predictions/) for details.

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
> EEZ boundaries represented by red lines on the map
> 
- ![Hotspot Map — 2000](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/hotspot_dynamics/maps/hotspots_2000.png)

**Hotspot Map - 2010 (Shifted Catch Hotspots)**
> EEZ boundaries represented by red lines on the map
> 
- ![Hotspot Map — 2010](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/hotspot_dynamics/maps/hotspots_2010.png)

**Hotspot Map - 2011 (Major Geographic Shift)**
> EEZ boundaries represented by red lines on the map
> 
- ![Hotspot Map — 2011](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/hotspot_dynamics/maps/hotspots_2011.png)

**Hotspot Map - 2020 (Post EEZ Enforcement)**
> EEZ boundaries represented by red lines on the map
> 
- ![Hotspot Map — 2020](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/hotspot_dynamics/maps/hotspots_2020.png)

**Animated Hotspot Shift - 2000, 2010, 2011, 2020**
- ![Animated Hotspot Shifts](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/hotspot_dynamics/maps/animated_hotspots.gif)

**Catch & CPUE Time Series**
- ![Catch Time Series](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/hotspot_dynamics/plots/squid_catch_cpue_over_time.png)

**Sample of Hotspots Colored by CPUE (Supplementary)**
- ![CPUE Hotspots](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/hotspot_dynamics/plots/sample_of_hotspots_colored_by_cpue.png)

---

> 📁 For more on spatio-temporal mapping, spatial database design, and geospatial
visual analytics using PostGIS and QGIS, see the other modules in the
GeoTentacles repository.
> 
