# 🌊 Toxic Tide Mapping — Pollution Level Spatial Prediction

## 🧭 Problem Framing & Decision Context
Marine ecosystems are impacted by multiple pollutants that vary spatially and temporally. Environmental consultancies and regulatory agencies need predictive tools to identify where contamination may occur to focus monitoring and management.  

This module predicts pollution intensity across squid catch regions using both chemical data and upstream human activity (industrial and agricultural outputs), producing actionable maps for decision-making.

## 📘 Executive Summary
- Input: pollutant chemistry, catch locations, industrial & agricultural indices
- Processing: Random Forest regression models to predict spatial pollution intensity across a regular grid
- Output: interactive maps of predicted pollution concentrations

**Key insights**
- Pollution hotspots are concentrated near high human activity areas
- Industrial and agricultural drivers explain lagged increases in contaminant levels

**Takeaway for decision-makers:** dynamic pollution maps enable targeted monitoring and intervention.

## 🌍 Real-World Value
- Prioritizes sampling in high-risk areas
- Supports scenario planning for pollution mitigation
- Integrates human pressure and environmental monitoring for evidence-based decision support

## 🎯 Applied Use Cases
- Pollution risk assessment and monitoring
- Policy planning and compliance prioritization
- Integration with marine health indices for ecological management

## 🧩 Module Overview

**Core Objectives**
- Predict spatial pollution intensity using ML regression
- Integrate chemical data with upstream drivers
- Visualize hotspots on interactive maps

**Outputs Generated**
- Predicted pollutant concentration grids
- Interactive Streamlit maps
- Summary tables for dashboard integration

**Interactive Features**
- Filter by tissue type, analyte, and month
- Hover for pollutant values and upstream pressures

**Insights Section**
- Dynamic plain-language explanations as the user toggles filters
- Explains why hotspots occur and which drivers contribute

## 🔧 Tools & Techniques
- Python: pandas, geopandas, scikit-learn (Random Forest Regressor)
- Streamlit for dashboard interactivity
- Plotly / Folium for spatial visualization

## 📈 Visual Outputs
- Interactive predicted pollution maps
- Grid-level heatmaps of contaminant intensity

## 📉 Limitations & Future Work
- Limited by sampling density
- Lag assumptions may vary across pollutants
- Future work: integrate ocean currents and seasonal effects

## 🧭 Summary Statement
Predictive pollution surfaces with integrated human pressures allow actionable identification of ecological risk areas in marine environments.
