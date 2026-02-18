# 🗺️ GeoTentacles — Spatial Analytics for Marine Species, Pollution & Habitat Dynamics

## 🌍 **Real-World Value** 

GeoTentacles transforms marine biological, chemical, and environmental datasets into spatial intelligence.  
It reveals *where* marine patterns occur, *how* they evolve, and *what* environmental factors shape them — using PostgreSQL/PostGIS, machine learning, and GIS workflows.

This repo supports:
- Fisheries agencies: mapping catch hotspots, effort distribution, and long-term spatial trends  
- Marine ecologists: linking species patterns to environmental drivers  
- Environmental groups: monitoring pollution levels and identifying risk zones  
- Data scientists: learning practical spatial analytics, geodata engineering, and ML for geospatial prediction  

GeoTentacles is the spatial “mapping wing” of the broader **Squid_Fest ecosystem**, complementing:
- **SquidStack** — deep biochemical & pollutant bioindicator exploration  
- **SquidStock** — long-term catch, environment, and predictive modeling  
- **GeoTentacles** — *the spatial dimension*, stitching catch, pollution, and environmental layers into geographic context  

🛂 **This repository hosts spatial workflows, datasets, prototypes, and dashboards.  
The full research pipeline lives in the private Squid_Fest repo — email me for collaboration.**

---

## 📂 Repository Structure

- `/sql` — PostGIS schema, spatial functions, index scripts
- `/spatial` — QGIS layers, GeoJSON exports, grids, rasters
- `/notebooks` — Exploratory spatial notebooks (Python + SQL)
- `/outputs` — Maps, hotspot layers, summary tables, rasters
- `/data` — Raw & processed geospatial datasets
- `/app` — Future interactive Streamlit spatial dashboards


---

## 📦 Project Modules & Flow

| Module | Stage Name | What It Does | Status | App |
|--------|------------|---------------|--------|------|
| **20-Year Squid Catch Hotspot Dynamics** | [**Charting the Currents**](https://github.com/Euchie23/GeoTentacles/tree/main/hotspot_dynamics) | Explore long-term squid catch hotspots (2000–2020) using PostGIS clustering, spatial grids, and density maps to understand where squids gather over time. | ✅ Completed | [🗺️ Hotspots Dashboard](<https://euchie23.shinyapps.io/geotentacles__hotspots/>) |
| **Squid Catch Hotspot Prediction (Classification)** | [**Forecasting the Swarms**](https://github.com/Euchie23/GeoTentacles/tree/main/hotspot_predictions) | Predict likely future squid catch hotspots with ML classification, helping fisheries anticipate and plan for swarming behavior. | ✅ Completed | 🗺️ Hotspots Dashboard |
| **Pollution Level Spatial Prediction (Regression)** | **Toxic Tide Mapping** |Map predicted pollution intensity across space using ML regression, interpolated grids, lagged squid catch, SST, SSH, Chlorophyll-a, and upstream human activity (industrial & agricultural pressures) to identify areas where contaminants may impact marine life. | 🟢 Planned | 🧪 Pollution & Marine Health Explorer |
| **Marine Pollution Interpolation (Kriging / IDW)** | **Seafloor Signals** | Transform raw pollutant chemistry points into smooth, continuous spatial surfaces using kriging and IDW interpolation for easier interpretation. | 🟢 Planned | 🧪 Pollution & Marine Health Explorer |
| **Marine Health Index (MCI)** | **EcoPulse Index** | Combine catch data, pollution data, habitat layers and human pressures into a single composite index that measures the overall health of marine ecosystems. | 🟢 Planned | 🧪 Pollution & Marine Health Explorer |
| **COVID-Impact Marine Health Model** | **Disruption Dynamics** | Analyze how marine ecosystems changed pre- vs post-COVID using spatial ML modeling, integrated with lagged environmental/catch metrics in addition to industrial/agricultural pressures, providing scenario-based insights for policy and management. | 🟢 Planned | 🔬 Scenario Simulator / Capstone |


---

## 🎯 Objectives

GeoTentacles aims to:

- Build reproducible spatial workflows for marine ecological datasets  
- Discover spatial hotspots of catch, pollution, and biological traits  
- Create predictive spatial models (classification + regression)  
- Generate continuous pollution surfaces via geostatistics  
- Construct composite health indices to support policy and management  
- Integrate catch + pollutant + environmental geodata, including upstream pressures, for multi-layer insights
- Develop interactive dashboards for visualization and decision support  

---

### 🛠 Tools & Techniques Used
**Spatial Database & Backend**
- PostgreSQL + PostGIS (geometry & geography columns, spatial indexing, tiling, grid creation)
- Cloud-hosted deployment for reproducible spatial SQL queries (NeonDB)

**GIS Tooling**
- QGIS (GeoJSON, shapefiles, rasters, WMS layers)
- Geospatial Python (geopandas, shapely, rasterio, pykrige / scikit-learn spatial ML)

**Machine Learning**
- Regression: Random Forest Regressor, GAMs, Gradient Boosting
- Spatial cross-validation (blocked CV)

**Dashboards**
- Streamlit with modular tabs (overview + each module)
- Optional Mapbox / Leaflet for interactive maps

---

### 📌 Data & Method Highlights
- Geometry creation: `ST_SetSRID(ST_MakePoint(lon, lat), 4326)`
- Distance metrics: `ST_Distance`, `ST_DWithin`
- Grid tiling: hex or square cells for hotspot stability
- Pollution interpolation: kriging, IDW, ML regression on grid averages
- Marine Health Index: normalized composite of pollution, catch, habitat, and human pressures
- Hotspot detection: DBSCAN, Getis-Ord, kernel density estimation

---

### 👥 Audience & Use Cases
- Marine ecologists & fisheries scientists
- Environmental monitoring agencies
- GIS analysts & data scientists
- Students in geospatial modeling 

---

## 📬 Get Involved

- 🐛 [Open an issue](https://github.com/Euchie23/GeoTentacles/issues) — suggestions, bugs, feature requests  
- ✉️ [Email me](mailto:euchiejnpierre@gmail.com) — for collaboration or access to related `Squid_Fest` resources  
- 💼 [Connect on LinkedIn](https://www.linkedin.com/in/euchiejnpierre/) — happy to discuss spatial work, marine science, or data  


---

> Thanks for checking out **GeoTentacles** -– the spatial foundations that bring squid-focused maps, models, and geospatial insights to life.
