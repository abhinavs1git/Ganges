-- Create PostGIS extension if it doesn't exist
CREATE EXTENSION IF NOT EXISTS postgis;

-- 1. Elevation Data Table
CREATE TABLE IF NOT EXISTS elevation_data (
    id SERIAL PRIMARY KEY,
    grid_id VARCHAR(50),
    elevation_meters FLOAT,
    geom GEOMETRY(Point, 4326)
);

-- 2. Rainfall Data Table
CREATE TABLE IF NOT EXISTS rainfall_data (
    id SERIAL PRIMARY KEY,
    station_name VARCHAR(100),
    date DATE,
    rainfall_mm FLOAT,
    geom GEOMETRY(Point, 4326)
);

-- 3. Rivers Data Table (OpenStreetMap)
CREATE TABLE IF NOT EXISTS rivers (
    id SERIAL PRIMARY KEY,
    river_name VARCHAR(100),
    waterway_type VARCHAR(50),
    geom GEOMETRY(LineString, 4326)
);

-- 4. Flood Risk Scores Table
CREATE TABLE IF NOT EXISTS flood_risk_scores (
    id SERIAL PRIMARY KEY,
    grid_id VARCHAR(50),
    elevation_meters FLOAT,
    rainfall_intensity FLOAT,
    distance_to_river_km FLOAT,
    risk_score FLOAT,
    risk_level VARCHAR(20),
    geom GEOMETRY(Point, 4326)
);

-- Create spatial indexes for faster querying
CREATE INDEX IF NOT EXISTS idx_elevation_geom ON elevation_data USING GIST(geom);
CREATE INDEX IF NOT EXISTS idx_rainfall_geom ON rainfall_data USING GIST(geom);
CREATE INDEX IF NOT EXISTS idx_rivers_geom ON rivers USING GIST(geom);
CREATE INDEX IF NOT EXISTS idx_flood_risk_geom ON flood_risk_scores USING GIST(geom);
