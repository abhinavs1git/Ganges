import os
import geopandas as gpd
import pandas as pd
import logging
import warnings
warnings.filterwarnings('ignore')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def standardize_crs(gdf, target_crs="EPSG:32644"):
    """
    Reproject to UTM Zone 44N (suitable for central/eastern UP) for accurate distance calculations in meters.
    """
    if gdf.crs != target_crs:
        logging.info(f"Reprojecting from {gdf.crs} to {target_crs}...")
        return gdf.to_crs(target_crs)
    return gdf

def run_preprocessing(base_path="../"):
    logging.info("Starting Data Preprocessing...")
    
    raw_rivers_path = os.path.join(base_path, "data/raw/rivers.geojson")
    raw_grid_path = os.path.join(base_path, "data/raw/basin_grid.geojson")
    
    if not os.path.exists(raw_rivers_path) or not os.path.exists(raw_grid_path):
        logging.error("Raw data not found. Please run data_pipeline.py first.")
        return
        
    rivers_gdf = gpd.read_file(raw_rivers_path)
    grid_gdf = gpd.read_file(raw_grid_path)
    
    logging.info("Standardizing Coordinate Systems...")
    # Standardize to UTM for metric distances
    rivers_proj = standardize_crs(rivers_gdf)
    grid_proj = standardize_crs(grid_gdf)
    
    # Data Cleaning (handling missing values, dropping invalid geoms)
    rivers_proj = rivers_proj[rivers_proj.geometry.is_valid & ~rivers_proj.geometry.is_empty]
    grid_proj = grid_proj[grid_proj.geometry.is_valid & ~grid_proj.geometry.is_empty]
    
    # Save processed base layers
    processed_dir = os.path.join(base_path, "data/processed")
    rivers_proj.to_file(os.path.join(processed_dir, "rivers_proj.gpkg"), driver="GPKG")
    grid_proj.to_file(os.path.join(processed_dir, "grid_proj.gpkg"), driver="GPKG")
    
    logging.info("Preprocessing complete. Processed data saved to data/processed.")

if __name__ == "__main__":
    base_proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    run_preprocessing(base_proj_dir)
