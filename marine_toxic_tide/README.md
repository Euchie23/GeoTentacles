# 🌊 Toxic Tide Mapping — Pollution Level Spatial Prediction

## 🧭 Problem Framing & Decision Context
Marine ecosystems are impacted by multiple pollutants that vary spatially and temporally. Environmental consultancies and regulatory agencies need predictive tools to identify where contamination may occur to focus monitoring and management.

This module predicts pollution intensity across squid catch regions using chemical data **and upstream human activity**, including industrial and agricultural outputs, as well as **lagged environmental and catch data** from 2018–2021 to capture delayed effects of both natural and anthropogenic factors.

## 📘 Executive Summary
- **Input:** pollutant chemistry, catch locations, industrial & agricultural indices, squid catch, and environmental data (SST, SSH, Chlorophyll-a, Depth)  
- **Processing:** ElasticNet regression models predict spatial pollution intensity across a regular grid, Predictions account for delayed effects captured via lagged environmental and catch data.
- **Output:** interactive maps of predicted pollution concentrations

**Key insights**
- Pollution hotspots correlate with high human activity areas and catch/lagged environmental signals  
- Lagged indicators reveal delayed pollution impacts

**Takeaway for decision-makers:** dynamic pollution maps enable targeted monitoring and intervention, incorporating temporal effects from human and environmental pressures.

## 🌍 Real-World Value
- Prioritizes sampling in high-risk areas  
- Supports scenario planning for pollution mitigation  
- Integrates human pressure, environmental data, and monitoring for robust evidence-based decision support, including tiered confidence levels for screening interpretation  

## 🎯 Applied Use Cases
- Pollution risk assessment and monitoring  
- Policy planning and compliance prioritization  
- Integration with marine health indices for ecological management
- Outputs include tiered confidence levels and model-derived risk signals, helping decision-makers prioritize locations for monitoring without over-interpreting absolute values.  

## 🧩 Module Overview

**Core Objectives**
- Predict spatial pollution intensity using ML regression  
- Incorporate chemical, environmental, and lagged human activity data  
- Visualize hotspots interactively  

**Outputs Generated**
- Predicted pollutant concentration grids  
- Interactive Streamlit maps  
- Summary tables for dashboard integration  

**Interactive Features**
- Filter by tissue type, analyte, and month  
- Hover for pollutant values, upstream pressures, and environmental indicators  

**Insights Section**
- Dynamic plain-language explanations  
- Explains why hotspots occur and which drivers contribute  

## 🔧 Tools & Techniques
- Python: pandas, geopandas, scikit-learn (ElasticNet regression)  
- Streamlit for dashboard interactivity  
- Plotly / Folium for spatial visualization
- Simplified distance-weighted pressure indices approximate spatial influence of human activities

## 📈 Visual Outputs
- Interactive predicted pollution maps  
- Grid-level heatmaps of contaminant intensity  

## 📉 Limitations & Future Work
- Limited by sampling density and spatial coverage  
- Lag assumptions may vary by pollutant
- Censored measurements reflect detection limits, not environmental processes. Including is_censored as a feature can bias predictions, especially for low-concentration pollutants. Interpret model outputs accordingly.
- Anomaly detection uses back-transformed residuals from log-modeled concentrations. Extreme values may reflect transformation effects, so interpret anomalies as screening indicators rather than definitive outliers.
- Incorporate ocean currents, seasonal effects, and additional environmental drivers  

## 🧭 Summary Statement
Predictive pollution surfaces with lagged human pressures and environmental data allow actionable identification of ecological risk areas in marine environments.

