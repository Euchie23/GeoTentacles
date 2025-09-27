# 🗺️ GeoTentacles — Spatial Analytics for Marine Species & Habitats

**GeoTentacles** is a spatial analytics offshoot of the larger `Squid_Fest` project. It aims to map the spatial distributions and environmental relationships of marine species using PostgreSQL, PostGIS, QGIS, and web‑based mapping tools. Though it’s in early stages, this repo already includes foundational schema and analysis scripts — and it’s set to grow into an interactive spatial analytics suite.

---

## 🌊 Positioning & Purpose

Think of **GeoTentacles** as the cartographer’s desk in your research ecosystem:  
- **SquidStack** dove into pollutant bioindicators — akin to exploring a remote, hidden trench — rare, rigorous, and deeply exploratory.  
- **SquidStock** surveys the broader shelf and coastal domain (including that trench), applying stock assessments, environmental modeling, and predictive tools to uncover patterns across more commonly traveled waters.  
- **GeoTentacles** focuses on the *where* — spatial structure, geographic patterns, and mapping the data that links stack & stock insights into place.

This repository is under active development. The README, module layout, and project content will evolve as scripts mature, spatial models are added, and dashboards go live.

---

## 📂 What You Can Explore Right Now

These are the features & scripts currently available:

- **PostgreSQL/PostGIS schema scripts** for tables like `squid_catch`, `concentrations`, `distance_land` with spatial (geometry/geography) columns  
- **Geometry update queries**: turning latitude/longitude into spatial geometry via `ST_SetSRID` and `ST_MakePoint`  
- **Spatial query prototypes**:
  - Distance joins: e.g. measuring how far squid catch points lie from land areas  
  - Aggregation by spatial bins (e.g. grouping by area, distance ranges)  
  - Linking concentration data to catch geometry to form pollutant spatial layers  
- **Indexing / performance scripts**: spatial indexing, geometry population, etc.

Even though these are early-stage, they set the base structure for the spatial analyses to come.

---

## 🔍 Planned GeoTentacles Projects (Tentative)

These are the future spatial modules I'm planning, to be added over time:

1. **Project 1 — Sampling Explorer (Map + Baseline Stats)**  
   *Story:* “Where and when did we sample? What’s the baseline distribution of biological traits?”  
   *Key tasks:* Create spatial table of samples, map sampling locations, filter by year/area/maturity, summary metadata, CSV export.  
   *Deliverables:* Postgres schema + seed scripts, QGIS snapshots, Streamlit map + summary UI.

2. **Project 2 (numbered “4” in your list) — Hotspot & Clustering Analysis**  
   *Story:* “Where are contamination hotspots, and are they persistent across years?”  
   *Key tasks:* Use clustering (e.g. KMeans), spatial aggregation (grid), Getis‑Ord hot spot analysis.  
   *Deliverables:* Hotspot SQL, GeoJSON exports, Streamlit hotspot maps & time animation, QGIS package.

3. **Project 3 (your “6”) — Risk Assessment & Compliance Mapper**  
   *Story:* “Which catches or zones exceed health thresholds — and what’s the risk if consumed or entering the supply chain?”  
   *Key tasks:* Join concentration and threshold tables, map exceedances, spatial intersections with fishing zones.  
   *Deliverables:* Map of exceedances, toggles per pollutant, “if consumed” calculator in UI, exportable maps & CSV.

4. **Project 4 (your “7”) — Spatio-Temporal Prediction (Interpolation & Uncertainty)**  
   *Story:* “Where are contaminant levels likely high in unsampled areas — with quantified uncertainty?”  
   *Key tasks:* Kriging / IDW modeling, convert predictions to raster / GeoTIFF, store in PostGIS.  
   *Deliverables:* Prediction pipeline, spatial raster layers, UI to visualize predictions + uncertainty.

*(Optional future module — Capstone StoryMap & Decision Support tool — not listed here yet, but may come later.)*

> 🔄 This README will be updated as modules mature. Project names, nicknames, and workflows will become more structured and navigable over time.

---

## 🛠 Tools & Technologies

Here’s the toolbox behind GeoTentacles and what’s planned:

- **Database / Spatial Backend:** PostgreSQL & PostGIS  
- **Spatial & GIS Tools:** QGIS (desktop), future plans for web mapping (Leaflet, Mapbox, etc.)  
- **Spatial SQL & Scripting:** native PostGIS functions (`ST_Distance`, `ST_DWithin`, `ST_MakePoint`, grid snapping, clustering, etc.)  
- **Integration Potential:** linking spatial layers with SquidStack pollutant data and SquidStock catch / environmental data  
- **Planned Libraries / Tools:** Geospatial Python (e.g. `geopandas`, `rasterio`), spatial modeling / interpolation (e.g. `pykrige`), web mapping stacks  

---

## ⚠️ Status & Notes

- This repository is **in progress** — many scripts are prototypes or drafts and may require refinement.  
- The spatial layers currently rely heavily on the existing catch & concentration tables with geometry fields. External environmental spatial layers (e.g. bathymetry, oceanographic rasters) are planned but not yet integrated.  
- As modules become more mature, this README will be reorganized with direct links, stable workflows, dashboards, and usage examples.

---

## 👥 Who This Seems Useful For

- GIS / spatial scientists interested in marine ecology  
- Students or researchers learning PostGIS and spatial modeling  
- Marine biologists wanting to link location to pollutant or biological data  
- Anyone curious about how space can add context to pollution, catch, and ecological patterns  

---

## 📬 Get Involved

- 🐛 [Open an issue](https://github.com/Euchie23/GeoTentacles/issues) — suggestions, bugs, feature requests  
- ✉️ [Email me](mailto:euchiejnpierre@gmail.com) — for collaboration or access to related `Squid_Fest` resources  
- 💼 [Connect on LinkedIn](https://www.linkedin.com/in/euchiejnpierre/) — happy to discuss spatial work, marine science, or data  

---

> Thanks for checking out **GeoTentacles**. Though it’s early, the spatial threads are already being laid. Return in the future to see maps, models, and dashboards emerge from these foundations.  
