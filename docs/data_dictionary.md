# UrbanFlow: Pune Traffic & Congestion Data Dictionary

This document provides a comprehensive specification of all tables, fields, data types, constraints, and domain interpretations used in the **UrbanFlow — Pune Traffic & Congestion Analysis** project.

---

## 1. Primary Table: `traffic_data`

* **Source**: Pune GTFS Traffic Prediction Dataset (Kaggle, authored by Charvi Bannur).
* **Granularity**: Stop-level transit segment observation per time slot.
* **Description**: Captures spatial location, transit route IDs, speed estimates under free-flow and congested conditions, calculated Speed Reduction Index (SRI), and categorical congestion ratings.

| Column Name | Data Type | Nullable | Primary Key / Index | Description & Research Context |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `BIGINT` | No | PK (Auto Increment) | Unique surrogate record identifier. |
| `route_id` | `VARCHAR(50)` | No | Indexed | PMPML public transit route identifier (e.g., `Route_101`). Enables corridor-level aggregation. |
| `stop_name` | `VARCHAR(255)` | No | Indexed | Official name of the bus stop / transit node in Pune urban area. |
| `latitude` | `DECIMAL(10, 7)` | No | None | Geographic latitude (WGS 84 coordinate reference system). |
| `longitude` | `DECIMAL(10, 7)` | No | None | Geographic longitude (WGS 84 coordinate reference system). |
| `time_slot` | `VARCHAR(50)` | No | None | Temporal observation window (e.g., `08:00 - 09:00` or `17:00:00`). |
| `speed_congested` | `DECIMAL(6, 2)` | No | None | Observed transit speed under actual prevailing traffic congestion ($\text{km/h}$). |
| `speed_freeflow` | `DECIMAL(6, 2)` | No | None | Reference benchmark transit speed under uncongested / free-flow conditions ($\text{km/h}$). |
| `sri` | `DECIMAL(6, 2)` | No | None | **Speed Reduction Index (%)**: Quantitative measure of speed loss relative to free-flow baseline. $SRI = \frac{v_{\text{freeflow}} - v_{\text{congested}}}{v_{\text{freeflow}}} \times 100$. |
| `congestion_level` | `VARCHAR(50)` | No | Indexed | Categorical Level of Service (LOS): `Very Smooth`, `Smooth`, `Mild Congestion`, `Heavy Congestion`. |
| `is_peak_hour` | `TINYINT(1)` | No | Indexed | Derived boolean indicator: `1` if observation falls in morning peak (8–10 AM) or evening peak (5–8 PM); `0` otherwise. |
| `created_at` | `TIMESTAMP` | No | Default `CURRENT_TIMESTAMP` | Ingestion timestamp in MySQL. |

---

## 2. Secondary Table: `vehicle_registrations`

* **Source**: OpenCity Urban Data Portal (Pune Municipal Corporation / RTO Aggregates).
* **Granularity**: Annual aggregation by vehicle category and fuel system.
* **Description**: Historical vehicle growth records used to contextualize macro traffic volume trends and modal split expansion in Pune.

| Column Name | Data Type | Nullable | Primary Key / Index | Description & Research Context |
| :--- | :--- | :--- | :--- | :--- |
| `id` | `INT` | No | PK (Auto Increment) | Unique surrogate row identifier. |
| `year` | `INT` | No | Indexed | Registration calendar year (e.g., `2015`, `2019`, `2022`). |
| `vehicle_type` | `VARCHAR(100)` | No | Indexed | Mode category: `Two-Wheeler`, `Four-Wheeler (Personal)`, `Auto-Rickshaw`, `Bus (PMPML / Private)`, `Goods Vehicle`. |
| `fuel_type` | `VARCHAR(50)` | No | Indexed | Fuel system: `Petrol`, `Diesel`, `CNG`, `Electric (EV)`, `Hybrid`. |
| `count` | `INT` | No | None | Total number of newly registered vehicles for the given category, year, and fuel type. |
| `created_at` | `TIMESTAMP` | No | Default `CURRENT_TIMESTAMP` | Ingestion timestamp in MySQL. |

---

## 3. Metrics & Derived Features Specification

### Speed Reduction Index (SRI)
$$\text{SRI} = \left( \frac{v_{\text{freeflow}} - v_{\text{congested}}}{v_{\text{freeflow}}} \right) \times 100\%$$
- **Interpretation**: 
  - $\text{SRI} = 0\%$: Zero congestion; transit operates at maximum design speed.
  - $\text{SRI} > 50\%$: Severe bottlenecking; speed degraded by over half relative to free-flow conditions.

### Peak Hour Windows (`is_peak_hour`)
- **Morning Peak**: 08:00 AM – 10:00 AM (`is_peak_hour = 1`)
- **Evening Peak**: 05:00 PM – 08:00 PM (`is_peak_hour = 1`)
- **Off-Peak**: All remaining hours (`is_peak_hour = 0`)
