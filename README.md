# UrbanFlow — Pune Traffic & Congestion Analysis

> **Research Question**: *Where and when is PMPML transit congestion most severe across Pune's urban network, and how do speed reduction indices vary across transit corridors, peak hours, and vehicle fleet expansion trends?*

---

## 📌 Project Overview

**UrbanFlow** is an empirical urban mobility research and data analysis project focused on public transit congestion patterns in Pune, India. Utilizing General Transit Feed Specification (GTFS) spatial-temporal traffic data combined with municipal vehicle registration figures, this repository provides a structured relational data pipeline, analytical SQL queries, and visual analytical frameworks for urban planners, transport researchers, and municipal policy analysts.

---

## 🛠 Tech Stack

* **Database & Storage**: MySQL 8.0+ (Relational schema, indexing, aggregation queries)
* **Data Ingestion & Cleaning**: Python 3.10+ (Pandas ETL, standard library `re`, `pathlib`)
* **Environment & Security**: `python-dotenv` for database credential management
* **Business Intelligence & Visualization**: Power BI Desktop (Interactive dashboards & spatial mapping)
* **Version Control**: Git & GitHub

---

## 📁 Repository Structure

```text
urbanflow-pune-traffic-analysis/
├── README.md                          # Project documentation & research findings
├── LICENSE                            # MIT Open Source License
├── .gitignore                         # Excludes secrets, bytecode, & raw data files
├── requirements.txt                   # Python package dependencies
├── .env.example                       # Database credentials template
├── data/
│   ├── raw/                           # Raw input CSV datasets (git-ignored)
│   └── processed/                     # Cleaned CSV ready for database loading
├── sql/
│   ├── schema.sql                     # MySQL database DDL table definitions
│   └── sample_queries.sql             # 5 research-focused analytical queries
├── scripts/
│   ├── config.py                      # Non-secret path & ETL configuration
│   ├── clean_data.py                  # Data cleaning & feature engineering script
│   ├── load_to_mysql.py               # Ingests cleaned traffic data to MySQL
│   └── load_vehicle_data.py           # Ingests secondary vehicle registrations data
├── powerbi/                           # Power BI dashboard files (.pbix)
└── docs/
    ├── data_dictionary.md             # Complete data dictionary for all schema tables
    └── screenshots/                   # Dashboard screenshots & spatial visual assets
```

---

## 📊 Datasets & Sources

1. **Primary Dataset: Pune GTFS Traffic Prediction Dataset**
   * **Source**: [Kaggle — Pune GTFS Traffic Prediction Dataset (by Charvi Bannur)](https://www.kaggle.com/)
   * **Description**: Contains transit route IDs, stop names, geographic coordinates (lat/long), time slots, free-flow speeds, congested speeds, Speed Reduction Index (SRI), and categorical congestion levels.

2. **Secondary Dataset: Pune Vehicle Registrations**
   * **Source**: [OpenCity Urban Data Portal](https://opencity.in/)
   * **Description**: Historical vehicle registration counts in Pune categorized by vehicle class (two-wheeler, four-wheeler, bus, auto-rickshaw), fuel system (petrol, diesel, CNG, EV), and registration year.

---

## ⚙️ Setup & Execution Guide

Follow these step-by-step instructions to set up the environment and run the pipeline:

### Step 1: Clone Repository & Create Virtual Environment
```bash
git clone https://github.com/your-username/urbanflow-pune-traffic-analysis.git
cd urbanflow-pune-traffic-analysis

python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
source venv/bin/activate
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment Variables
Copy `.env.example` to `.env` and fill in your local MySQL database credentials:
```bash
cp .env.example .env
```
Edit `.env`:
```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_actual_password
DB_NAME=urbanflow_pune
```

### Step 4: Prepare Data Files
Place raw CSV dataset files inside `data/raw/`:
* `data/raw/pune_gtfs_traffic.csv` (Primary GTFS traffic dataset)
* `data/raw/pune_vehicle_registrations.csv` (Secondary vehicle registrations dataset)

### Step 5: Execute Data Cleaning & Feature Engineering
Run the cleaning script to handle missing attributes, standardize text, and compute peak-hour flags:
```bash
python scripts/clean_data.py
```
*Output*: Generates `data/processed/traffic_clean.csv`.

### Step 6: Initialize MySQL Database Schema
Execute `sql/schema.sql` in MySQL Workbench or via MySQL Command Line Client:
```bash
mysql -u root -p < sql/schema.sql
```

### Step 7: Load Data into MySQL
Ingest cleaned CSV datasets into relational tables:
```bash
python scripts/load_to_mysql.py
python scripts/load_vehicle_data.py
```

### Step 8: Run Analytical SQL Queries
Execute the analytical query suite in `sql/sample_queries.sql` to generate insights on bottleneck stops, time-of-day speed losses, and route congestion rankings.

---

## 🔬 Research Methodology

### 1. Speed Reduction Index (SRI)
Congestion intensity is evaluated using the **Speed Reduction Index (SRI)**, defined as:

$$\text{SRI} = \left( \frac{v_{\text{freeflow}} - v_{\text{congested}}}{v_{\text{freeflow}}} \right) \times 100\%$$

* **Higher SRI %**: Represents greater operational speed loss relative to uncongested baseline.
* **SRI Classification**:
  * `Very Smooth`: $0\% \le \text{SRI} < 15\%$
  * `Smooth`: $15\% \le \text{SRI} < 35\%$
  * `Mild Congestion`: $35\% \le \text{SRI} < 55\%$
  * `Heavy Congestion`: $\text{SRI} \ge 55\%$

### 2. Peak Hour Derivation
Operating slots are categorized into bimodal rush-hour windows:
* **Morning Peak**: `08:00 AM - 10:00 AM`
* **Evening Peak**: `05:00 PM - 08:00 PM`
* **Off-Peak**: All remaining transit hours.

---

## ⚠️ Research Limitations

1. **Temporal Snapshot Scope**: The primary GTFS dataset represents a single-period baseline snapshot and does not capture seasonal variations, severe monsoon flooding disruptions, or holiday traffic shifts.
2. **Static GTFS vs. Real-Time Telematics**: Speed estimates are calculated based on scheduled transit arrival windows and segment distances, which may vary from actual high-frequency GPS vehicle tracking logs.
3. **Secondary Data Temporal Granularity**: Vehicle registration statistics are published as annual aggregates and cannot be disaggregated into daily corridor-level volume estimates without micro-simulation modeling.

---

## 📈 Key Findings (Placeholder)

*(Fill in after running SQL analytical queries and building Power BI visualizations)*

* **Peak Hour Speed Degradation**: [Insert % speed reduction observed during 8-10 AM vs off-peak]
* **Top Bottleneck Corridor**: [Insert highest SRI transit stop / route ID]
* **Network Level of Service**: [Insert percentage share of Heavy vs Smooth congestion records]

---

## 🖼 Dashboard & Visualizations (Placeholder)

*(Add Power BI dashboard screenshots into `docs/screenshots/` and link them below)*

![Power BI Overview Placeholder](docs/screenshots/overview_dashboard.png)
*Figure 1: Pune Transit Congestion Spatial Hotspots & Temporal Speed Reduction Dashboard.*

---

## 📜 License

This project is licensed under the [MIT License](LICENSE) — free for academic, research, and commercial use.
