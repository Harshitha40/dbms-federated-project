import requests

DRILL_URL = "http://localhost:8047/query.json"

# Try combining Postgres tables to reduce CTE count
query = """
WITH 
pg_combined AS (
    SELECT 
        r.region_id,
        r.region_name,
        c.temperature,
        c.rainfall,
        a.crop_type,
        a.`yield` as crop_yield
    FROM postgres.public.`region_info` r
    LEFT JOIN postgres.public.`climate_data` c ON r.region_id = c.region_id
    LEFT JOIN postgres.public.`agriculture_data` a ON r.region_id = a.region_id
),
mongo_bio AS (SELECT region_id, species_count FROM mongo.environmental_db.`Biodiversity_Data`),
csv_sensors AS (SELECT CAST(region_id AS INT) as rid, CAST(co2_level AS FLOAT) as co2, CAST(pm2_5 AS FLOAT) as pm FROM dfs.data.`sensor_readings.csv`)
SELECT 
    p.region_name,
    p.temperature,
    p.rainfall,
    p.crop_type,
    p.crop_yield,
    b.species_count,
    s.co2 as co2_level,
    s.pm as pm2_5
FROM pg_combined p
LEFT JOIN mongo_bio b ON p.region_id = b.region_id
LEFT JOIN csv_sensors s ON s.rid = p.region_id
LIMIT 15
"""

try:
    response = requests.post(DRILL_URL, json={"queryType": "SQL", "query": query}, timeout=30)
    data = response.json()
    
    if data.get('queryState') == 'COMPLETED':
        rows = data.get('rows', [])
        print(f"SUCCESS! {len(rows)} rows returned")
        print("\nFirst 3 rows:")
        for i, row in enumerate(rows[:3]):
            print(f"{i+1}. {row}")
    else:
        print("FAILED")
        
except Exception as e:
    print(f"Exception: {e}")
