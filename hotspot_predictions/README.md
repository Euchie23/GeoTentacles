# 🦑 Forecasting the Swarms — Predicting Squid Catch Hotspots Using Machine Learning

## 📘 Executive Summary

### What we did
Developed a Random Forest classification model to estimate squid catch hotspot likelihood using spatially aggregated environmental and catch data derived from **hotspot_dynamics**. Predictions were generated for independent test years (2016–2020), restricted to the January–June period to align with peak aggregation and data availability.

### Main outcomes
- Predicted probability surfaces reveal coherent and ecologically plausible spatial patterns during years with strong aggregation signals (2016–2018)
- Predictive discrimination weakens in later years (2019–2020), consistent with reduced aggregation and weaker spatial structure rather than model instability
- Probability-based outputs provide a more transparent and informative representation of uncertainty than binary classification alone

### Why it matters
This approach emphasizes **habitat suitability and aggregation potential**, not fishing effort, enabling cautious and interpretable hotspot prediction suitable for applied decision-making.

### Data scope
A 20-year squid catch dataset aggregated to 0.25° × 0.25° polygon grid cells, paired with environmental variables including sea surface temperature (SST), bathymetry, sea surface height (SSH), and chlorophyll-a.

---

## 🌍 Real-World Value

This module extends the spatial hotspot framework developed in **hotspot_dynamics** by adding forward-looking, probability-based hotspot prediction. Using the same polygon grid and environmental covariates, it supports proactive planning where aggregation patterns are expected to change over time.

### Who This Helps
- **Fisheries managers:** prioritize survey effort under uncertainty  
- **Environmental consultancies:** support spatial risk screening and planning  
- **NGOs & practitioners:** explore interannual variability in habitat suitability  

This module is designed to complement retrospective hotspot mapping by identifying **relative aggregation risk**, not guaranteed fishing outcomes.

---

## 🎯 Applied Use Case — Risk-Aware Spatial Planning

**Example scenario:**  
If a monitoring program were planned for 2018, polygons with predicted hotspot probability above a conservative threshold (e.g., >0.4) could be prioritized for survey allocation. Lower-probability regions would remain candidates for background sampling, ensuring spatial coverage while focusing limited resources on areas with higher aggregation potential.

This approach supports **risk-aware prioritization** without assuming guaranteed catch or stable hotspot persistence.

---

## 🧱 Modeling Workflow & Data Lineage
This project uses polygon-level features derived from hotspot_dynamics outputs.

### Workflow overview
1. Polygon-level features derived from hotspot_dynamics outputs  
2. Environmental and catch summaries assembled into a modeling feature table  
3. Random Forest classifier trained on historical data  
4. Predictions generated for independent test years (2016–2020)  
5. Outputs exported to PostGIS for validation, visualization, and dashboard use  

All predictions are served from PostgreSQL/PostGIS to support reproducible analysis and future Shiny integration.

---

## 🧩 Module Objectives

### Core Objectives
- Predict squid catch hotspot likelihood at the polygon level  
- Quantify uncertainty using probability-based outputs  
- Validate predictions using multiple complementary metrics  
- Prepare spatial outputs for interactive and client-facing deployment  

### Outputs Generated
- Hotspot probability maps by year (2016–2020)  
- Binary hotspot classification maps  
- Validation figures (probability bins, calibration curves, ROC/AUC)  
- Confusion matrices and performance summaries  
- Serialized model and results objects (`.qs`) for Shiny runtime  

---

## 🔧 Tools & Techniques

### Core Stack
- **PostgreSQL + PostGIS:** spatial feature storage and serving  
- **R:** modeling, validation, and visualization  
- **Random Forest:** tree-based classification with probabilistic outputs  
- **Shiny (planned):** interactive exploration and decision support  

### Key Methods
- Temporal hold-out validation using independent test years  
- Multi-metric evaluation (discrimination, calibration, spatial plausibility)  
- Conservative thresholding to minimize false positives  

---

## 📊 Model Validation & Results

> **Interpretation note:**  
> Interannual variation in validation performance reflects differences in squid aggregation strength and ecological conditions across years, rather than model instability. Results should be interpreted conservatively, especially in years with weak spatial structure.


### 1️⃣ Hotspot Probability Validation
Predicted probabilities were grouped into bins and compared against observed mean catch. All validation metrics and spatial predictions reflect January–June conditions only and should be interpreted as seasonal, not annual, performance.

**Key findings**
- Mean observed catch generally increases with predicted probability in most years  
- High-probability bins contain relatively few observations, reflecting hotspot rarity  
- No high-probability predictions occur in 2020 

**Figure:** Observed Catch by Predicted Hotspot Probability
![**Observed Hotspot Probability**](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/hotspot_predictions/maps/hotspot_probability_by_year.png)

**Figure:** Hotspot Probability Validation
![**Hotspot Probability Validation**](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/hotspot_predictions/plots/hotspot_probability_validation.png)

---

### 2️⃣ Calibration Curves
Calibration curves were used to assess how well predicted probabilities align with observed hotspot frequencies.

**Key findings**
- Reasonable calibration during years with strong spatial structure (2016–2018)  
- Reduced calibration in later years, with fewer positive cases  
- Probabilities remain conservative rather than overconfident  

**Figure:** Calibration Curves by Year - multi-panel calibration plot (2016–2020)
![**Calibration Curves**](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/hotspot_predictions/plots/calibration_curve_by_year.png)

---

### 3️⃣ Binary Hotspot Classification
Probability outputs were thresholded to produce binary hotspot predictions suitable for operational use.

**Key findings**
- High true-negative rates across all years  
- True positives concentrated in earlier years with stronger aggregation  
- Conservative predictions with limited false-positive classification  

**Figure:** Predicted Hotspots by Year (Binary Classification) 
![**Binary Hotspot Prediction**](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/hotspot_predictions/maps/predicted_hotspots_by_year.png)

---

### 4️⃣ Discrimination Performance (ROC / AUC)

**AUC by year**
- 2016: **0.776**  
- 2017: **0.670**  
- 2018: **0.651**  
- 2019: **0.574**  
- 2020: **0.584**

Overall discrimination is consistently above random expectations across all years

**Figure:** ROC Curves and AUC Scores by Year
![**Roc_Curve_By_Year**](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/hotspot_predictions/plots/roc_curve_by_year.png)

📁 For full validation outputs (confusion matrices, calibration bin tables, and extended ROC metrics), see [Validation Folder](https://github.com/Euchie23/GeoTentacles/blob/main/outputs/hotspot_predictions/plots/)


---

## 🌱 Ecological Interpretation
Predicted hotspot probabilities show a consistent northward concentration during 2016–2018, followed by weakened spatial structure in 2019 and a near absence of high-probability hotspots in 2020. This pattern aligns with known squid life-history dynamics along the Patagonian Shelf, including feeding migrations and spawning-related movements. All spatial patterns reflect conditions, corresponding to known seasonal migration and aggregation phases in the squid life cycle.


Notably, predicted hotspots often occur slightly north of observed catch locations, suggesting the model captures **environmental suitability and aggregation potential**, rather than simply reproducing historical fishing effort.

---

## 🔒 Data Confidentiality Notice
This dataset is a simulated approximation of a real-world squid stock assessment dataset used during my tenure as a part-time research assistant at National Taiwan University. While it closely resembles operational data, results presented here should be interpreted as methodological demonstrations rather than real-world stock assessments.

---

## 📉 Limitations & Considerations
- Hotspots are rare events, leading to limited high-probability observations  
- Temporal coverage and sampling intensity vary across years  
- Model discrimination declines during periods of weak aggregation  
- Predictions reflect environmental suitability, not fishing accessibility or effort  

These limitations reflect ecological variability and data constraints rather than model instability.

---

## 🧭 Summary Statement
This module demonstrates how spatial hotspot analysis can be extended into **probabilistic, forward-looking prediction** using machine learning, while maintaining transparency and ecological interpretability. Together with **hotspot_dynamics**, it forms a coherent pipeline from historical mapping to applied decision support.

---

## 🔗 Relationship to hotspot_dynamics
This project is a direct continuation of **hotspot_dynamics — 20-Year Spatio-Temporal Hotspot Analysis of Squid Catch**. hotspot_dynamics establishes the spatial foundation and aggregation logic, while this module adds predictive capability and uncertainty-aware outputs.

---

## 📸 Visual Outputs (Selected)

| Visualization | Purpose |
|--------------|--------|
| Hotspot Probability Maps | Identify relative likelihood of aggregation |
| Binary Hotspot Maps | Conservative decision-support outputs |
| Probability Validation | Link predictions to observed catch |
| Calibration Curves | Assess probability reliability |
| ROC / AUC | Evaluate discrimination performance |

---

## 🧪 Shiny Integration (In Progress)
All model outputs, validation metrics, and spatial predictions are stored as serialized `.qs` files and PostGIS tables to support interactive exploration in a Shiny application. Planned functionality includes:
- Adjustable probability thresholds  
- Year-by-year comparison  
- Probability vs binary views  
- On-demand performance diagnostics  

---

## 🤝 Collaboration & Contact
Contributions and extensions are welcome, particularly in:
- Fisheries ecology and habitat modeling  
- Applied spatio-temporal ML workflows  
- Interactive geospatial dashboards  

📬 [Email](mailto:euchiejnpierre@gmail.com) | [LinkedIn](https://www.linkedin.com/in/euchiejnpierre/)

---

> 📁 For more on spatio-temporal mapping, spatial database design, and geospatial
visual analytics using PostGIS and QGIS, see the other modules in the
GeoTentacles repository.
> 
