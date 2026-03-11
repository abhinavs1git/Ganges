import os
import geopandas as gpd
import pandas as pd
import numpy as np
import logging
from sklearn.preprocessing import MinMaxScaler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_flood_risk(base_path="../"):
    logging.info("Starting Flood Risk Modeling...")
    
    in_path = os.path.join(base_path, "data/processed/analysis_ready.gpkg")
    out_path = os.path.join(base_path, "outputs/flood_risk_results.gpkg")
    
    if not os.path.exists(in_path):
        logging.error("Analysis ready data not found. Run spatial_analysis.py first.")
        return
        
    df = gpd.read_file(in_path)
    
    # Ensure columns exist
    required_cols = ['elevation_meters', 'rainfall_mm', 'distance_to_river_km']
    for col in required_cols:
        if col not in df.columns:
            logging.error(f"Missing required column: {col}")
            return
            
    # Risk factors directionality:
    # High Rainfall -> Higher Risk (Positive)
    # High Elevation -> Lower Risk (Negative correlation) -> Invert
    # High Distance to River -> Lower Risk (Negative correlation) -> Invert
    
    scaler = MinMaxScaler()
    
    logging.info("Normalizing variables...")
    # Normalize Rainfall directly (0 to 1)
    df['norm_rainfall'] = scaler.fit_transform(df[['rainfall_mm']])
    
    # Normalize Elevation to 'Low Elevation Score' (0 to 1) where lower elevation = closer to 1
    elev_norm = scaler.fit_transform(df[['elevation_meters']])
    df['norm_low_elevation'] = 1 - elev_norm # Invert so low elev = high score
    
    # Normalize Distance to River to 'River Proximity Score' (0 to 1) where closer to river = closer to 1
    dist_norm = scaler.fit_transform(df[['distance_to_river_km']])
    df['norm_river_proximity'] = 1 - dist_norm # Invert
    
    logging.info("Computing Flood Risk Score...")
    # Apply weights: 40% Rainfall, 30% River Prox, 30% Low Elevation
    df['risk_score'] = (
        0.4 * df['norm_rainfall'] + 
        0.3 * df['norm_river_proximity'] + 
        0.3 * df['norm_low_elevation']
    )
    
    # Rescale absolute score to 0-100 for interpretability
    df['risk_score_100'] = df['risk_score'] * 100
    
    # Classify Risk Levels
    # Typical classes: Low (< 33), Medium (33-66), High (> 66)
    def classify_risk(score):
        if score > 66: return 'High Risk'
        elif score > 33: return 'Medium Risk'
        else: return 'Low Risk'
        
    df['risk_level'] = df['risk_score_100'].apply(classify_risk)
    
    # Reproject to WGS84 for visualization (maps/dashboards)
    df_wgs = df.to_crs("EPSG:4326")
    
    logging.info("Saving modeled results...")
    df_wgs.to_file(out_path, driver="GPKG")
    # Also save as GeoJSON for the web map explicitly
    df_wgs.to_file(out_path.replace(".gpkg", ".geojson"), driver="GeoJSON")
    
    logging.info("Flood Risk Modeling Complete!")
    return df_wgs

if __name__ == "__main__":
    base_proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    calculate_flood_risk(base_proj_dir)
