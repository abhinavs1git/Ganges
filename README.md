# 🌊 Ganga Basin Flood Risk Analysis

![Project Banner](https://img.shields.io/badge/Project-Data_Analytics-blue.svg) ![Status](https://img.shields.io/badge/Status-Completed-success.svg)

## 📌 Project Overview

Flooding is a recurring challenge across many regions of the Ganga Basin in Uttar Pradesh, India. This project analyzes flood risk by combining environmental factors and visualizing high-risk areas through an interactive Tableau dashboard.

The goal is to identify locations that may require greater attention during flood seasons and provide a simple, data-driven approach for risk assessment.

---

## 🎯 Objective

Determine flood-prone areas using three key factors:

* **Elevation** – Lower elevations are generally more susceptible to flooding.
* **Rainfall** – Areas receiving higher rainfall face increased flood risk.
* **Distance from River** – Locations closer to rivers are more vulnerable during overflow events.

---

## 📂 Dataset

The project uses CSV files containing:

### 1. Elevation Data

* Location coordinates
* Elevation (meters)

### 2. Rainfall Data

* Location coordinates
* Annual rainfall (mm)

### 3. River Data

* River coordinates and reference points

### 4. Flood Risk Scores

* Calculated flood risk score
* Assigned risk category

---

## 🛠️ Methodology

### Step 1: Data Preparation

* Load datasets from CSV files
* Clean and validate records
* Merge datasets based on location

### Step 2: Distance Calculation

* Calculate the distance between each location and the nearest river point

### Step 3: Risk Scoring

Three factors are normalized on a scale of 0–1:

* Higher rainfall = Higher risk
* Lower elevation = Higher risk
* Shorter river distance = Higher risk

### Risk Formula

Risk Score =

(0.4 × Rainfall) +
(0.3 × River Proximity) +
(0.3 × Low Elevation)

Final scores are scaled from **0–100**.

### Risk Categories

| Score Range | Risk Level |
| ----------- | ---------- |
| 0 – 33      | Low        |
| 34 – 66     | Medium     |
| 67 – 100    | High       |

---

## 🚀 How to Run

### Install Requirements

```bash
pip install -r requirements.txt
```

### Run Analysis

```bash
python flood_risk_analysis.py
```

The script:

* Reads input CSV files
* Calculates risk scores
* Generates the final output CSV

Output files are saved in:

```text
outputs/
```

---

## 📊 Tableau Dashboard

The processed data is visualized in Tableau to support flood-risk assessment.

### Dashboard Features

#### Interactive Risk Map

Displays locations categorized as:

* 🔴 High Risk
* 🟠 Medium Risk
* 🟢 Low Risk

#### KPI Cards

Shows:

* Total Locations Analyzed
* Average Risk Score
* High-Risk Area Percentage

#### Risk Analysis Visuals

* Risk Score Distribution
* Rainfall vs Risk Score
* Distance from River vs Risk Score

---

## 📈 Key Insights

* Locations near rivers consistently show higher flood risk.
* Low-lying areas become significantly more vulnerable when combined with high rainfall.
* Risk categorization helps quickly identify priority zones for monitoring and preparedness.

---

## 🧰 Tools Used

* Python
* Pandas
* NumPy
* Tableau
* CSV Data Processing

---

## 📁 Project Structure

```text
Ganga-Flood-Risk-Analysis/
│
├── data/
│   ├── elevation_data.csv
│   ├── rainfall_data.csv
│   └── river_data.csv
│
├── outputs/
│   └── flood_risk_scores.csv
│
├── dashboard/
│   └── tableau_dashboard.twb
│
├── notebooks/
│   └── analysis.ipynb
│
├── flood_risk_analysis.py
├── requirements.txt
└── README.md
```

## 📊 Tableau Dashboard Visualization
Rather than hosting custom web code, we use **Tableau Community / Public Version** to present findings, making this project highly suitable for business intelligence roles. 

### Key Dashboard Features:
* **Interactive Map**: Displays grid locations colored by risk level (Red: High, Orange: Medium, Green: Low).
* **KPI Metric Cards**: Displays Total points analyzed, Average Risk score, and % of High Risk areas.
* **Analysis Scatter Plots**: Visualizes the mathematical decay curve showing how risk drops as distance from rivers increases.

<img width="1363" height="766" alt="image" src="https://github.com/user-attachments/assets/d64422c4-4c15-4b9d-95be-77bb54580db7" />

---

## 💡 Key Insights
* **Elevation Structuring**: Proximity to water is a key risk factor, but ground elevation plays a massive role. Points close to a river on high ground might be safer than deep basins miles away.
* **Actionable Priorities**: By bucketing scores into High, Medium, and Low risk, regional disaster management teams can instantly pinpoint hot-spot zones for reinforcements.
---
