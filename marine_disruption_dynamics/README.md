# 🌊 Disruption Dynamics — COVID Impact on Marine Health

## 🧭 Problem Framing & Decision Context
COVID-related reductions in human activity provide a natural experiment for ecosystem response. This module now incorporates **lagged industrial/agricultural indices and environmental/catch data from 2018–2020** to better interpret pre- vs post-COVID changes.

## 📘 Executive Summary
- **Input:** EcoPulse Index per tissue, industrial & agricultural activity, lagged environmental/catch indicators  
- **Processing:** temporal comparison using 2019–2020 data, with lagged pressures  
- **Output:** pre/post-COVID maps, trend plots, dynamic insights  

**Key insights**
- Ecosystem improvements are clearer when accounting for lagged human and environmental pressures  
- Legacy pollution or persistent pressures are highlighted  

**Takeaway for decision-makers:** identify sensitive regions and plan interventions using robust, multi-layer data.

## 🌍 Real-World Value
- Scenario-based policy guidance  
- Highlights lagged effects of human activity on ecosystems  
- Supports monitoring, research, and resource allocation  

## 🎯 Applied Use Cases
- Policy evaluation: measure ecosystem response to human activity reduction  
- Targeted monitoring and restoration  
- Integration with predictive modeling for future scenarios  

## 🧩 Module Overview

**Core Objectives**
- Compare pre- vs post-COVID EcoPulse scores  
- Incorporate industrial & agricultural pressures with lag  
- Integrate lagged environmental catch data (2018–2020)  
- Generate maps, trend plots, and plain-language insights  

**Outputs Generated**
- Interactive maps of EcoPulse pre/post-COVID  
- Time-series plots of human pressures  
- Dynamic insights section for non-technical interpretation  

**Interactive Features**
- Select tissue type and years  
- Include/exclude transition year 2020  
- Insights section explains trends in plain language  

## 🔧 Tools & Techniques
- Python: pandas, geopandas, plotly  
- Streamlit for interactive dashboards  
- Lagged feature engineering for pressure indices  

## 📈 Visual Outputs
- Pre/post COVID EcoPulse maps  
- Trend lines of industrial/agricultural activity  
- Hoverable interactive elements  

## 📉 Limitations & Future Work
- Data gaps and uneven sampling  
- Lag assumptions approximate  
- Future: include environmental drivers (SST, currents) for mechanistic insights  

## 🧭 Summary Statement
Disruption Dynamics quantifies ecosystem responses to human activity changes during COVID, integrating lagged pressures to support evidence-based management and scenario planning.
