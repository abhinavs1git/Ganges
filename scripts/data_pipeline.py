import os
import ssl
import urllib.request
import zipfile
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Disable SSL verification for simple downloads if needed
ssl._create_default_https_context = ssl._create_unverified_context

def create_directory_structure(base_path="../"):
    """Creates the standard data directory structure."""
    dirs = [
        "data/raw",
        "data/processed",
        "outputs/maps",
        "outputs/plots"
    ]
    for d in dirs:
        os.makedirs(os.path.join(base_path, d), exist_ok=True)
    logging.info("Project directory structure verified/created.")

def download_mock_data(base_path="../"):
    """
    Downloads or generates mock sample data for the Ganga Basin.
    In a real-world scenario, this replaces automated downloads from NASA EARTHDATA or IMD.
    """
    logging.info("Generating sample geospatial datasets for Ganga Basin, UP...")
    
    # Generate mock River Data (simplified Ganga and Yamuna)
    rivers = gpd.GeoDataFrame({
        'river_name': ['Ganga', 'Yamuna', 'Ghaghara'],
        'waterway_type': ['river', 'river', 'river']
    }, geometry=gpd.GeoSeries.from_wkt([
        'LINESTRING(78.0 29.5, 80.0 27.0, 83.0 25.5, 84.0 25.0)', # Pseudo Ganga
        'LINESTRING(77.5 29.0, 78.5 28.0, 80.0 27.0)',            # Pseudo Yamuna
        'LINESTRING(81.0 28.5, 82.5 27.0, 83.5 25.8)'             # Pseudo Ghaghara
    ]), crs="EPSG:4326")
    rivers.to_file(os.path.join(base_path, "data/raw/rivers.geojson"), driver="GeoJSON")

    # Generate mock grid points (Elevation & Rainfall) across UP
    # UP bounding box approx: Lon: 77.0 to 84.5, Lat: 23.5 to 30.5
    import numpy as np
    np.random.seed(42)
    lons = np.random.uniform(77.0, 84.5, 1000)
    lats = np.random.uniform(23.5, 30.5, 1000)
    
    # Closer to rivers (lower elevation and higher rainfall theoretically in a basin)
    elevations = np.random.uniform(50, 400, 1000) # 50m to 400m
    rainfalls = np.random.uniform(400, 1500, 1000) # 400mm to 1500mm annually
    
    points = [Point(lon, lat) for lon, lat in zip(lons, lats)]
    grid_gdf = gpd.GeoDataFrame({
        'grid_id': [f'GRID_{i}' for i in range(1000)],
        'elevation_meters': elevations,
        'rainfall_mm': rainfalls
    }, geometry=points, crs="EPSG:4326")
    
    grid_gdf.to_file(os.path.join(base_path, "data/raw/basin_grid.geojson"), driver="GeoJSON")
    logging.info("Mock raw data generated and saved to data/raw.")

def execute_pipeline():
    logging.info("Starting Data Pipeline...")
    base_proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    create_directory_structure(base_proj_dir)
    download_mock_data(base_proj_dir)
    logging.info("Data Pipeline: Raw Data Acquisition Complete.")

if __name__ == "__main__":
    execute_pipeline()
