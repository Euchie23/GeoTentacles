# 🦑 Forecasting the Swarms — Predicting Squid Catch Hotspots Using Machine Learning

## 🌍 Real-World Value
This module extends the spatial hotspot framework developed in **hotspot_dynamics** by introducing predictive modeling. Using the same polygon grid system, spatial aggregation logic, and environmental covariates, this project applies machine-learning classification to estimate the **probability of squid catch hotspots** across multiple years.

Rather than reproducing historical fishing patterns, the model identifies **environmentally suitable regions for squid aggregation**, supporting proactive planning and risk-based decision-making.

**Who This Helps**
- Fisheries managers: anticipate likely hotspot regions under varying conditions  
- Environmental consultancies: support spatial planning and monitoring strategies  
- NGOs & researchers: explore habitat suitability and interannual variability  

**Why It Matters**
Hotspots are dynamic. Predicting where they are *likely* to occur — and quantifying uncertainty — provides a stronger foundation for adaptive management than retrospective mapping alone.

---

## 📘 Executive Summary
**What we did:**  
Built a Random Forest classification model to predict squid catch hotspot likelihood using spatially aggregated environmental and catch data derived from Project A. Predictions were generated as continuous probability surfaces and thresholded into binary hotspot classifications.

**Main outcomes:**
- Hotspot probability surfaces reveal coherent spatial patterns in years with strong aggregation signals (2016–2018)
- Model confidence and discrimination weaken in later years (2019–2020), consistent with reduced aggregation and data coverage
- Probability-based outputs provide a more informative and cautious representation than binary classification alone

**Why it matters:**  
This approach captures habitat suitability and aggregation potential rather than fishing effort alone, enabling more ecologically meaningful and transparent hotspot predictions.

**Data scope:**  
20-year squid catch dataset aggregated to 0.25° × 0.25° polygon grid cells, with environmental variables including SST, depth, SSH, and chlorophyll-a.

---

## 🧱 Modeling Workflow & Data Lineage
This project directly builds on the spatial database, polygon grid, and aggregation logic established in **Project A**. No new spatial discretization was introduced.

**Workflow overview:**
1. Polygon-level features generated from Project A outputs  
2. Environmental and catch summaries assembled into an ML feature table  
3. Random Forest classification trained on historical years  
4. Predictions generated for independent test years (2016–2020)  
5. Outputs exported to PostGIS for validation and interactive use  

All predictions are served from PostgreSQL/PostGIS to support reproducible analysis and Shiny integration.

---

## 🧩 Module Objectives
**Core Objectives**
- Predict squid catch hotspot likelihood at the polygon level
- Quantify uncertainty using probability-based outputs
- Validate predictions using multiple complementary metrics
- Prepare spatial outputs for interactive dashboard deployment

**Outputs Generated**
- Probability maps by year (2016–2020)
- Binary hotspot classification maps
- Validation figures (probability bins, calibration curves, ROC/AUC)
- Confusion matrices and performance summaries
- Serialized model and results objects (`.qs`) for Shiny runtime

---

## 🔧 Tools & Techniques

**Core Stack**
- **PostgreSQL + PostGIS:** feature storage and spatial serving layer  
- **R:** modeling, validation, and visualization  
- **Random Forest:** tree-based classification with probabilistic outputs  
- **Shiny (planned):** interactive exploration and decision support  

**Key Methods**
- Probability-based classification rather than deterministic labeling  
- Temporal hold-out validation (training vs independent test years)  
- Multi-metric model evaluation (discrimination, calibration, ecological plausibility)  
- Conservative thresholding to avoid overconfident predictions  

---

## 📊 Model Validation & Results

### 1️⃣ Hotspot Probability Validation
Predicted probabilities were grouped into bins and compared against observed mean catch.

**Figure:** Hotspot Probability Validation (Mean Catch by Probability Bin)  
*Insert PNG here*

Key findings:
- Mean observed catch generally increases with predicted probability (2016–2019)
- High-probability bins contain few observations, reflecting hotspot rarity
- No high-probability predictions in 2020, consistent with weak aggregation signals

---

### 2️⃣ Calibration Curves
Calibration curves were used to assess probability reliability across years.

**Figure:** Calibration Curves by Year  
*Insert PNG here*

Key findings:
- Reasonable calibration during strong aggregation years (2016–2018)
- Degraded calibration in later years, reflecting environmental variability and sparse sampling

---

### 3️⃣ Binary Hotspot Classification
Probability outputs were thresholded to produce binary hotspot maps.

**Figure:** Predicted Hotspots by Year (Binary Classification)  
*Insert PNG here*

Key findings:
- High true-negative rates across all years
- True positives concentrated in earlier years
- Conservative behavior under weak signal conditions

---

### 4️⃣ Discrimination Performance (ROC / AUC)

**Figure:** ROC Curves and AUC Scores by Year  
*Insert PNG here*

- Overall AUC: **0.649**
- Strong discrimination in 2016 and 2018
- Near-random discrimination in 2019–2020, consistent with reduced spatial structure

---

## 🌱 Ecological Interpretation
Predicted hotspot probabilities exhibit a clear northward concentration during 2016–2018, followed by a weakening pattern in 2019 and a near-absence of high-probability hotspots in 2020. This spatial signal aligns with the known squid life cycle, including southward feeding migrations along the Patagonian Shelf and subsequent northward movement toward spawning grounds.

Importantly, predicted hotspots often occur north of observed catch locations, suggesting that the model identifies environmentally suitable aggregation or pre-spawning regions rather than reproducing historical fishing effort alone.

---

## 📉 Limitations & Considerations
- Hotspots are rare, leading to sparse high-probability observations  
- Temporal coverage is uneven across years and seasons  
- Model performance declines during years with weak aggregation signals  
- Predictions reflect environmental suitability, not fishing effort or accessibility  

These limitations reflect data availability and ecological variability rather than overfitting or model instability.

---

## 🧭 Summary Statement
This module demonstrates how spatial hotspot analysis can be extended into **probabilistic prediction** using machine learning, while maintaining ecological interpretability and transparency. Together with Project A, it forms a coherent analytical pipeline from historical mapping to forward-looking decision support.

---

## 🔗 Relationship to Project A
This project is a direct continuation of **Project A — 20-Year Spatio-Temporal Hotspot Analysis of Squid Catch**. Project A establishes the spatial foundation and aggregation logic, while Project B builds predictive capability on top of that framework.

---

## 📸 Visual Outputs (Selected)

| Visualization | Description |
|---------------|-------------|
| Hotspot Probability Maps | Continuous probability surfaces by year |
| Binary Hotspot Maps | Thresholded hotspot predictions |
| Probability Validation | Mean observed catch by probability bin |
| Calibration Curves | Probability reliability by year |
| ROC / AUC | Discrimination performance |

---

## 🧪 Shiny Integration (In Progress)
All model outputs, validation objects, and predictions are stored as serialized `.qs` files and PostGIS tables to support interactive exploration in a Shiny application. Users will be able to:
- Adjust probability thresholds
- Explore year-specific predictions
- Compare probability and binary views
- Review model performance metrics

---

## 🤝 Collaboration & Contact
Contributions and extensions are welcome, particularly in:
- Fisheries ecology and habitat modeling
- Spatio-temporal ML workflows
- Interactive geospatial dashboards

📬 [Email](mailto:euchiejnpierre@gmail.com) | [LinkedIn](https://www.linkedin.com/in/euchiejnpierre/)

---

## 🔒 Data Confidentiality Notice
This dataset is a simulated approximation of a real-world squid stock assessment dataset. While structurally realistic, it should not be interpreted as representing actual fishery conditions.

