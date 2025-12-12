# 🌊 Charting the Currents — 20-Year Spatio-Temporal Hotspot Analysis of *Illex argentinus*

## 🌍 Real-World Value
This module provides operational hotspot maps for the squid species *Illex argentinus* using 20 years of vessel-level catch data enriched with environmental variables.  
It answers a central fisheries question:

> Where do fishing hotspots form, how do they shift across decades, and which environmental factors drive those shifts?

### Who This Helps
- **Fisheries agencies** – seasonal closures, effort regulation  
- **Marine spatial planners** – multi-year distribution patterns  
- **Ecosystem-based managers** – understanding SST/chlorophyll drivers  
- **GIS & data science teams** – reproducible spatial analytics workflows  

### Why It Matters
CPUE alone gives no spatial context. Hotspot analysis reveals where fleets concentrate effort and where environmental features align with catch intensity — crucial for sustainable management.

## 📘 Executive Summary
**What we built:**  
- A fully spatial, PostGIS-powered pipeline  
- 0.25° grid-cell aggregation of 100k+ georeferenced fishing events  
- Year-by-year hotspot layers linked to environmental variables  
- QGIS visualizations + outputs for future Shiny/Streamlit apps  

**Core outputs include:**  
- Annual hotspot maps  
- Vessel-day effort maps  
- Environmental overlays (SST, SSH, chlorophyll-a)  
- Aggregated hotspot table (`analysis.squid_hotspots`)  
- Public view for apps (`public.squid_hotspot_view`)  

**Key findings (to update after analysis):**  
- Strong, persistent hotspots along [X] frontal boundary  
- Warm-year shifts toward the south in 2009, 2014  
- Chlorophyll-a consistently aligned with high-catch cells  
- Vessel concentration influences hotspot intensity  

## 🧩 Module Overview  
**“Mapping 20 Years of Spatial Hotspots”**

**Objectives**
- Build foundations: raw → core → analysis PostGIS schemas  
- Clean and spatialize 20-year squid catch data  
- Aggregate points into 0.25° cells  
- Compute multi-year vessel-day effort  
- Create professional QGIS hotspot maps  
- Produce layers and views for interactive dashboards  

## 🗺️ Spatial Analysis Framework
- Data Preparation: raw → core → analysis → geometry + indices  
- Grid-Cell Aggregation: 0.25° grid per year → catch, effort, CPUE  
- QGIS Mapping: heatmaps, graduated layers, temporal animations  
- Outputs for Dashboards: `public.squid_hotspot_view`

## 🛠️ Tools & Techniques
- PostgreSQL + PostGIS  
- QGIS  
- Python (GeoPandas, Matplotlib, SQLAlchemy)  
- SQL aggregation, spatial indexing, temporal analysis  

## 📊 Outputs
- Maps: `/outputs/maps/`  
- Tables: `/outputs/tables/hotspot_summary.csv`  
- Layers: `/spatial/*.geojson`, `/spatial/*.gpkg`  

## 📉 Limitations & Future Work
- Monthly environmental variables limit fine-scale temporal matching  
- Grid size fixed at 0.25°  
- No dynamic fleet behavior modeling  
- Future Project B: CPUE standardization, GAMs, predictive modeling  

## 🧭 Summary
This module establishes a reproducible geospatial analytics pipeline for fisheries data using PostGIS + QGIS. It reveals long-term hotspot patterns, generates GIS-ready layers, and forms the foundation for dashboarding and ecological modeling.

## 🤝 Contact
Open to collaboration—especially with fisheries, GIS, or climate researchers.

