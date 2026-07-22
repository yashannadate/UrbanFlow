-- UrbanFlow: Pune Traffic & Congestion Analytical Queries
USE urbanflow_pune;

-- Query 1: Temporal Congestion Profile — Average SRI and Speeds by Time Slot
-- Goal: Identify peak congestion windows across the transit network
SELECT 
    time_slot,
    COUNT(*) AS total_observations,
    ROUND(AVG(sri), 2) AS avg_sri,
    ROUND(AVG(speed_congested), 2) AS avg_congested_speed_kmh,
    ROUND(AVG(speed_freeflow), 2) AS avg_freeflow_speed_kmh
FROM traffic_data
GROUP BY time_slot
ORDER BY avg_sri DESC;

-- Query 2: Spatial Hotspot Analysis — Top 10 Most Congested Bus Stops
-- Goal: Pinpoint critical bottlenecks using average Speed Reduction Index
SELECT 
    stop_name,
    COUNT(DISTINCT route_id) AS connecting_routes,
    COUNT(*) AS total_records,
    ROUND(AVG(sri), 2) AS avg_sri,
    ROUND(AVG(speed_congested), 2) AS avg_speed_kmh,
    SUM(CASE WHEN congestion_level = 'Heavy Congestion' THEN 1 ELSE 0 END) AS heavy_congestion_instances
FROM traffic_data
GROUP BY stop_name
HAVING COUNT(*) >= 3
ORDER BY avg_sri DESC
LIMIT 10;

-- Query 3: Severity Breakdown — Distribution and Share of Congestion Levels
-- Goal: Quantify overall network level of service (LOS)
SELECT 
    congestion_level,
    COUNT(*) AS record_count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM traffic_data), 2) AS percentage_share,
    ROUND(AVG(sri), 2) AS avg_sri
FROM traffic_data
GROUP BY congestion_level
ORDER BY avg_sri DESC;

-- Query 4: Peak vs Non-Peak Operating Performance
-- Goal: Contrast transit efficiency during peak demand hours vs off-peak hours
SELECT 
    CASE WHEN is_peak_hour = 1 THEN 'Peak Hours (8-10AM, 5-8PM)' ELSE 'Non-Peak Hours' END AS period_type,
    COUNT(*) AS record_count,
    ROUND(AVG(speed_congested), 2) AS avg_congested_speed_kmh,
    ROUND(AVG(speed_freeflow), 2) AS avg_freeflow_speed_kmh,
    ROUND(AVG(sri), 2) AS avg_sri,
    ROUND(((AVG(speed_freeflow) - AVG(speed_congested)) / AVG(speed_freeflow)) * 100, 2) AS speed_loss_percentage
FROM traffic_data
GROUP BY is_peak_hour;

-- Query 5: Route Congestion Ranking
-- Goal: Rank PMPML transit corridors by severity of congestion index
SELECT 
    route_id,
    COUNT(DISTINCT stop_name) AS total_stops,
    ROUND(AVG(sri), 2) AS avg_route_sri,
    ROUND(MIN(speed_congested), 2) AS min_recorded_speed_kmh,
    ROUND(AVG(speed_congested), 2) AS avg_congested_speed_kmh,
    SUM(CASE WHEN congestion_level IN ('Heavy Congestion', 'Mild Congestion') THEN 1 ELSE 0 END) AS congested_stop_counts
FROM traffic_data
GROUP BY route_id
ORDER BY avg_route_sri DESC;
