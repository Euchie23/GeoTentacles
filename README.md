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

## 🖥️ Interactive Dashboards

GeoTentacles provides two key dashboards for spatial insight and decision support:

### 🗺️ Hotspots
**Historical and Predicted Catch or Pollution Hotspots** — Track long-term trends and anticipate future events in marine species distribution.

![Hotspots Screenshot](https://drive.google.com/uc?export=view&id=16QFd0BjXcCvKwhat1yurb5nd4y4adsEn)

[🚀 Launch Hotspots Dashboard](https://euchie23.shinyapps.io/geotentacles__hotspots/)

[🎥 Watch the 5-Minute Guided Tour](https://youtu.be/vKbAumUKFQU)

---

### 🌎 MarineScope
**The Window into Marine Health** — Maps pollution, ecosystem condition, and environmental change with continuous surfaces and composite indices.

![MarineScope Screenshot](https://drive.google.com/uc?export=view&id=18ME9ue0aXP4RuhggHhYc5Df9usN9qiCU)

[🚀 Launch MarineScope Dashboard](https://geotentacles-marinescope.streamlit.app)

[🎥 Watch the 5-Minute Guided Tour](https://youtu.be/m0ECpnxTsNI)

---

## 📂 Repository Structure

- `/sql` — PostGIS schema, spatial functions, index scripts
- `/scripts` — R and Python Scripts for ML and App Creation
- `/spatial` — QGIS layers, GeoJSON exports, grids, rasters
- `/notebooks` — Exploratory spatial notebooks (Python + SQL)
- `/outputs` — Maps, hotspot layers, summary tables
- `/data` — Raw & processed geospatial and predictor datasets
- `/app` — Interactive Streamlit spatial dashboards


---

## 📦 Project Modules & Flow

| Module | Stage Name | What It Does | Status | App |
|--------|------------|---------------|--------|------|
| **20-Year Squid Catch Hotspot Dynamics** | [**Charting the Currents**](https://github.com/Euchie23/GeoTentacles/tree/main/hotspot_dynamics) | Explore long-term squid catch hotspots (2000–2020) using PostGIS clustering, spatial grids, and density maps to understand where squids gather over time. | ✅ Completed | [🗺️ Hotspots Dashboard](<https://euchie23.shinyapps.io/geotentacles__hotspots/>) |
| **Squid Catch Hotspot Prediction (Classification)** | [**Forecasting the Swarms**](https://github.com/Euchie23/GeoTentacles/tree/main/hotspot_predictions) | Predict likely future squid catch hotspots with ML classification, helping fisheries anticipate and plan for swarming behavior. | ✅ Completed | 🗺️ Hotspots Dashboard |
| **Pollution Level Spatial Prediction (Regression)** | [**Toxic Tide Mapping**](https://github.com/Euchie23/GeoTentacles/blob/main/notebooks/marine_toxic_tide/toxic_tide_mapping.ipynb) |Map predicted pollution intensity across space using ML regression, interpolated grids, lagged squid catch, SST, SSH, Chlorophyll-a, and upstream human activity (industrial & agricultural pressures) to identify areas where contaminants may impact marine life. | ✅ Completed | [🌐 MarineScope Dashboard](https://geotentacles-marinescope.streamlit.app)|
| **Marine Pollution Interpolation (IDW)** | **Seafloor Signals** | Transform raw pollutant chemistry points into smooth, continuous spatial surfaces using kriging and IDW interpolation for easier interpretation. | ✅ Completed | 🌐 MarineScope Dashboard |
| **Marine Health Index (MCI)** | **EcoPulse Index** | Combine catch data, pollution data, habitat layers and human pressures into a single composite index that measures the overall health of marine ecosystems. | ✅ Completed | 🌐 MarineScope Dashboard |
| **COVID-Impact Marine Health Model** | **Disruption Dynamics** | Analyze how marine ecosystems changed pre- vs post-COVID using spatial ML modeling, integrated with lagged environmental/catch metrics in addition to industrial/agricultural pressures, providing scenario-based insights for policy and management. | ✅ Completed | 🌐 MarineScope Dashboard |


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
- Regression: Random Forest Regressor, Elastic Net
- Spatial cross-validation (blocked CV)

**Dashboards**
- Streamlit with modular tabs (overview + each module)
- Optional Mapbox / Leaflet for interactive maps

---

### 📌 Data & Method Highlights
- Geometry creation: `ST_SetSRID(ST_MakePoint(lon, lat), 4326)`
- Distance metrics: `ST_Distance`, `ST_DWithin`
- Grid tiling: hex or square cells for hotspot stability
- Pollution interpolation: IDW, ML regression on grid averages
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
