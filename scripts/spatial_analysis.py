import os
import geopandas as gpd
import pandas as pd
import logging
import numpy as np
from shapely.ops import nearest_points

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_elevation_and_distances(base_path="../"):
    """
    Computes distance to nearest river for each grid point and prepares the analytic dataset.
    """
    logging.info("Starting Spatial Analysis...")
    
    processed_dir = os.path.join(base_path, "data/processed")
    rivers_path = os.path.join(processed_dir, "rivers_proj.gpkg")
    grid_path = os.path.join(processed_dir, "grid_proj.gpkg")
    
    if not os.path.exists(rivers_path) or not os.path.exists(grid_path):
        logging.error("Processed data missing. Run preprocessing.py first.")
        return
        
    rivers_proj = gpd.read_file(rivers_path)
    grid_proj = gpd.read_file(grid_path)
    
    # 1. Compute Distance to nearest River
    logging.info("Calculating Distance to Nearest River...")
    # For large datasets, a spatial index or sjoin_nearest is required.
    # We will use geopandas sjoin_nearest.
    
    joined = gpd.sjoin_nearest(
        grid_proj, rivers_proj, how='left', distance_col='distance_to_river_m'
    )
    
    # Ensure no duplicates if multiple rivers are equidistant
    analysis_ready = joined.drop_duplicates(subset=['grid_id']).copy()
    
    # Optional: If dealing with raw DEM Tiffs, we would sample raster here
    # Since we mocked elevation into the grid earlier, we skip rasterio extraction here.
    # In real world: extract_raster_val = [x[0] for x in rasterio.sample.sample_gen(raster, points)]
    
    # Convert distance to KM for easier interpretability
    analysis_ready['distance_to_river_km'] = analysis_ready['distance_to_river_m'] / 1000.0
    
    out_path = os.path.join(processed_dir, "analysis_ready.gpkg")
    analysis_ready.to_file(out_path, driver="GPKG")
    logging.info(f"Spatial Analysis Complete. Saved output to {out_path}.")

if __name__ == "__main__":
    base_proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    extract_elevation_and_distances(base_proj_dir)
