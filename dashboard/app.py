import streamlit as st
import geopandas as gpd
import folium
import plotly.express as px
from streamlit_folium import folium_static
import os

st.set_page_config(page_title="Ganges - Flood Risk Dashboard", layout="wide")

@st.cache_data
def load_data():
    base_proj_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_path = os.path.join(base_proj_dir, "outputs/flood_risk_results.geojson")
    rivers_path = os.path.join(base_proj_dir, "data/raw/rivers.geojson")
    
    results = gpd.read_file(results_path) if os.path.exists(results_path) else None
    rivers = gpd.read_file(rivers_path) if os.path.exists(rivers_path) else None
    
    return results, rivers

st.title("🌊 Ganges - Flood Risk Mapping for the Ganga Basin, UP")
st.markdown("Geospatial analysis of flood risk driven by Rainfall, Elevation, and River Proximity.")

results, rivers = load_data()

if results is None:
    st.error("Data not found. Please run scripts/run_all.py or individual scripts first to generate outputs.")
else:
    # Quick Stats
    st.header("Project Overview & Statistics")
    
    col1, col2, col3 = st.columns(3)
    avg_risk = results['risk_score_100'].mean()
    high_risk_pct = (len(results[results['risk_level'] == 'High Risk']) / len(results)) * 100
    
    col1.metric("Total Grid Points Analyzed", len(results))
    col2.metric("Average Flood Risk Score", f"{avg_risk:.1f}/100")
    col3.metric("% High Risk Areas", f"{high_risk_pct:.1f}%")

    # Map Section
    st.header("Interactive Risk Map")
    
    # Calculate map center based on bounds
    bounds = results.total_bounds
    center_y = (bounds[1] + bounds[3]) / 2
    center_x = (bounds[0] + bounds[2]) / 2
    
    m = folium.Map(location=[center_y, center_x], zoom_start=7, tiles='CartoDB Voyager')
    
    colors = {'Low Risk': 'green', 'Medium Risk': 'orange', 'High Risk': 'red'}
    
    # Add points
    for idx, row in results.iterrows():
        folium.CircleMarker(
            location=[row.geometry.y, row.geometry.x],
            radius=4,
            popup=f"Risk: {row['risk_score_100']:.1f} | Level: {row['risk_level']}<br>Elev: {row['elevation_meters']:.0f}m",
            color=colors.get(row['risk_level'], 'blue'),
            fill=True,
            fill_opacity=0.7
        ).add_to(m)
        
    # Add rivers
    if rivers is not None:
        folium.GeoJson(rivers, name="Rivers", style_function=lambda x: {'color': 'blue', 'weight': 2}).add_to(m)
    
    folium_static(m, width=1000, height=500)

    st.header("Exploratory Data Analysis")
    colA, colB = st.columns(2)
    
    with colA:
        fig_dist = px.histogram(results, x="risk_score_100", color="risk_level", title="Risk Score Distribution", 
            color_discrete_map=colors)
        st.plotly_chart(fig_dist, use_container_width=True)
        
    with colB:
        fig_scatter = px.scatter(results, x="distance_to_river_km", y="risk_score_100", color="risk_level", 
            title="Distance to River vs Risk Score", color_discrete_map=colors)
        st.plotly_chart(fig_scatter, use_container_width=True)
