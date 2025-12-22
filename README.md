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

| Module | Stage Name | What It Does | Status | Link | App |
|--------|------------|---------------|--------|-------|------|
| **20-Year Squid Catch Hotspot Dynamics** | **Charting the Currents** | Explore long-term squid catch hotspots (2000–2020) using PostGIS clustering, spatial grids, and density maps to understand where squids gather over time. | 🟢 Planned | 🔗 TBD | 🗺️ Hotspots Dashboard |
| **Squid Catch Hotspot Prediction (Classification)** | **Forecasting the Swarms** | Predict likely future squid catch hotspots with ML classification, helping fisheries anticipate and plan for swarming behavior. | 🟢 Planned | 🔗 TBD | 🗺️ Hotspots Dashboard |
| **Pollution Level Spatial Prediction (Regression)** | **Toxic Tide Mapping** | Map predicted pollution intensity across space using ML regression and interpolated grids, identifying areas where contaminants may impact marine life. | 🟢 Planned | 🔗 TBD | 🧪 Pollution & Marine Health Explorer |
| **Marine Pollution Interpolation (Kriging / IDW)** | **Seafloor Signals** | Transform raw pollutant chemistry points into smooth, continuous spatial surfaces using kriging and IDW interpolation for easier interpretation. | 🟢 Planned | 🔗 TBD | 🧪 Pollution & Marine Health Explorer |
| **Marine Health Index (MCI)** | **EcoPulse Index** | Combine catch, pollution, and habitat layers into a single composite index that measures the overall health of marine ecosystems. | 🟢 Planned | 🔗 TBD | 🧪 Pollution & Marine Health Explorer |
| **COVID-Impact Marine Health Model** | **Disruption Dynamics** | Analyze how marine ecosystems changed pre- vs post-COVID with spatial ML modeling, providing scenario-based insights for policy and management. | 🟢 Planned | 🔗 TBD | 🔬 Scenario Simulator / Capstone |


---

## 🎯 Objectives

GeoTentacles aims to:

- Build reproducible spatial workflows for marine ecological datasets  
- Discover spatial hotspots of catch, pollution, and biological traits  
- Create predictive spatial models (classification + regression)  
- Generate continuous pollution surfaces via geostatistics  
- Construct composite health indices to support policy and management  
- Integrate catch + pollutant + environment geodata for multi-layer insights  
- Develop interactive dashboards for visualization and decision support  

---

## 🛠 Tools & Techniques Used

### **Spatial Database & Backend**
- PostgreSQL + PostGIS  
- Geometry & geography columns  
- Spatial indexing (GiST), tiling, grid creation  

### **GIS Tooling**
- QGIS  
- GeoJSON, shapefiles, rasters, WMS layers  

### **Geospatial Python**
- geopandas  
- shapely  
- rasterio  
- pykrige / scikit-learn spatial ML  

### **Machine Learning**
- Classification: Random Forest, Gradient Boosting, XGBoost (grid-aggregated)  
- Regression: Random Forest Regressor, GAMs, Gradient Boosting  
- Spatial cross-validation (blocked CV)  

### **Dashboards**
- Streamlit (planned)  
- Mapbox / Leaflet (optional future expansion)  

---

## 📌 Data & Method Highlights

- **Geometry creation:**  
  `ST_SetSRID(ST_MakePoint(lon, lat), 4326)`  
- **Distance-to-land or zone:**  
  `ST_Distance`, `ST_DWithin`  
- **Grid tiling:**  
  hex or square cells for hotspot stability  
- **Pollution interpolation:**  
  kriging, IDW, ML regression on grid averages  
- **Hotspot detection:**  
  DBSCAN, Getis-Ord, kernel density estimation  
- **Marine Health Index:**  
  normalized scores across pollution, catch, distance, etc.  

---

## 👥 Audience & Use Cases

This project is valuable for:

- Marine ecologists  
- Fisheries scientists  
- Environmental monitoring agencies  
- GIS analysts  
- Data scientists learning spatial ML  
- Students in geospatial modeling  

---

## 📬 Get Involved

- 🐛 [Open an issue](https://github.com/Euchie23/GeoTentacles/issues) — suggestions, bugs, feature requests  
- ✉️ [Email me](mailto:euchiejnpierre@gmail.com) — for collaboration or access to related `Squid_Fest` resources  
- 💼 [Connect on LinkedIn](https://www.linkedin.com/in/euchiejnpierre/) — happy to discuss spatial work, marine science, or data  


---

> Thanks for checking out **GeoTentacles** -– the spatial foundations that bring squid-focused maps, models, and geospatial insights to life.
