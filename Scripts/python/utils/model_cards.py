def describe_model(model_name):
    cards = {
        "environment_only": {
            "title": "Environmental Conditions Model",
            "description": """
            Estimates pollution levels based on oceanographic conditions such as temperature,
            depth, sea surface height, and chlorophyll concentration.
            
            Missing data are handled using typical values observed in the dataset,
            and inputs are normalized to ensure no single variable dominates predictions.
            """
        },

        "env_plus_catch": {
            "title": "Environment + Fisheries Interaction Model",
            "description": """
            Builds on environmental conditions by incorporating squid catch intensity,
            which acts as a proxy for biological interaction and ecosystem exposure.
            
            Data gaps are automatically corrected, and variables are balanced to ensure
            stable and comparable influence across predictors.
            """
        },

        "full_pressures": {
            "title": "Human Pressure Exposure Model",
            "description": """
            Integrates environmental conditions with distance-weighted industrial and
            agricultural activity upstream.
            
            Pollution sources closer to the sampling location contribute more strongly
            than distant sources, reflecting realistic spatial dispersion.
            """
        },

        "full_pressures_plus_censoring": {
            "title": "Regulatory-Aware Exposure Model",
            "description": """
            Combines environmental drivers, fisheries activity, and upstream human pressures
            while explicitly accounting for laboratory detection limits.
            
            This model is designed for regulatory and risk-assessment contexts, ensuring
            predictions remain stable even when measurements fall below detection thresholds.
            """
        }
    }

    return cards.get(
        model_name,
        {
            "title": "Unknown Model",
            "description": "No description available for the selected model."
        }
    )


