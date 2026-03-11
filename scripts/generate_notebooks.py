import json
import os

def create_notebook(filename, cells):
    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    with open(filename, 'w') as f:
        json.dump(notebook, f, indent=2)

def md_cell(text):
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [text]
    }

def code_cell(code):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [code]
    }

def generate_eda_notebook(base_path):
    cells = [
        md_cell("# Exploratory Spatial Data Analysis (ESDA)\n\nThis notebook explores the raw metrics for the Ganga Basin: Elevation, Rainfall, and Rivers."),
        code_cell("import geopandas as gpd\nimport matplotlib.pyplot as plt\nimport os\n\nbase_dir = '../data/raw'\n# Load data\nrivers = gpd.read_file(os.path.join(base_dir, 'rivers.geojson'))\ngrid = gpd.read_file(os.path.join(base_dir, 'basin_grid.geojson'))\n\nprint('Rivers:', rivers.shape)\nprint('Grid points:', grid.shape)"),
        md_cell("## Visualizing Initial Layers"),
        code_cell("fig, ax = plt.subplots(figsize=(10, 8))\ngrid.plot(column='elevation_meters', ax=ax, legend=True, cmap='terrain', alpha=0.5)\nrivers.plot(ax=ax, color='blue', linewidth=2)\nax.set_title('Elevation Map with Major Rivers (Ganga Basin)')\nplt.show()"),
        md_cell("## Rainfall Distribution"),
        code_cell("fig, ax = plt.subplots(figsize=(10, 8))\nscatter = grid.plot(column='rainfall_mm', ax=ax, legend=True, cmap='Blues', alpha=0.7, markersize=10)\nrivers.plot(ax=ax, color='blue', linewidth=1)\nax.set_title('Rainfall Map (mm) across Uttar Pradesh')\nplt.show()")
    ]
    create_notebook(os.path.join(base_path, "01_exploratory_spatial_data_analysis.ipynb"), cells)

def generate_model_notebook(base_path):
    cells = [
        md_cell("# Flood Risk Modeling\n\nWe apply a weighted spatial approach to determine flood likelihood."),
        code_cell("import geopandas as gpd\nimport pandas as pd\nimport numpy as np\nfrom sklearn.preprocessing import MinMaxScaler\n\ngdf = gpd.read_file('../data/processed/analysis_ready.gpkg')\ngdf.head()"),
        md_cell("## Standardizing Features\nWe use MinMaxScaler to cast all variables between 0-1."),
        code_cell("scaler = MinMaxScaler()\ngdf['norm_rain'] = scaler.fit_transform(gdf[['rainfall_mm']])\ngdf['norm_prox'] = 1 - scaler.fit_transform(gdf[['distance_to_river_km']])\ngdf['norm_elev'] = 1 - scaler.fit_transform(gdf[['elevation_meters']])\n\ngdf['risk_score'] = (0.4 * gdf['norm_rain']) + (0.3 * gdf['norm_prox']) + (0.3 * gdf['norm_elev'])\ngdf['risk_score_100'] = gdf['risk_score'] * 100\n\ngdf['risk_score_100'].describe()")
    ]
    create_notebook(os.path.join(base_path, "02_flood_risk_modeling.ipynb"), cells)

def generate_vis_notebook(base_path):
    cells = [
        md_cell("# Interactive Visualizations and Heatmaps\n\nGenerating final risk map outputs for decision makers."),
        code_cell("import geopandas as gpd\nimport folium\n\nresults = gpd.read_file('../outputs/flood_risk_results.geojson')\n\n# Calculate center\nbounds = results.total_bounds\ny = (bounds[1] + bounds[3]) / 2\nx = (bounds[0] + bounds[2]) / 2\n\nm = folium.Map(location=[y, x], zoom_start=7)\nresults.explore(column='risk_level', cmap='RdYlGn_r', m=m)\nm")
    ]
    create_notebook(os.path.join(base_path, "03_visualizations.ipynb"), cells)

if __name__ == '__main__':
    os.makedirs('../notebooks', exist_ok=True)
    generate_eda_notebook('../notebooks')
    generate_model_notebook('../notebooks')
    generate_vis_notebook('../notebooks')
    print("Notebooks generated successfully.")
