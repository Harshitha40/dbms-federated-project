import requests

DRILL_URL = "http://localhost:8047/query.json"

# New approach: 3 CTEs total - one per DATA SOURCE
# Postgres CTE will handle all 3 Postgres tables via subquery
query = """
WITH 
postgres_data AS (
    SELECT 
        r.region_id,
        r.region_name,
        (SELECT temperature FROM postgres.public.`climate_data` c WHERE c.region_id = r.region_id LIMIT 1) as temperature,
        (SELECT rainfall FROM postgres.public.`climate_data` c WHERE c.region_id = r.region_id LIMIT 1) as rainfall,
        (SELECT crop_type FROM postgres.public.`agriculture_data` a WHERE a.region_id = r.region_id LIMIT 1) as crop_type,
        (SELECT `yield` FROM postgres.public.`agriculture_data` a WHERE a.region_id = r.region_id LIMIT 1) as crop_yield
    FROM postgres.public.`region_info` r
),
mongo_data AS (
    SELECT region_id, species_count 
    FROM mongo.environmental_db.`Biodiversity_Data`
),
csv_data AS (
    SELECT CAST(region_id AS INT) as region_id, CAST(co2_level AS FLOAT) as co2, CAST(pm2_5 AS FLOAT) as pm 
    FROM dfs.data.`sensor_readings.csv`
)
SELECT 
    p.region_name,
    p.temperature,
    p.rainfall,
    p.crop_type,
    p.crop_yield,
    m.species_count,
    c.co2 as co2_level,
    c.pm as pm2_5
FROM postgres_data p
LEFT JOIN mongo_data m ON p.region_id = m.region_id
LEFT JOIN csv_data c ON p.region_id = c.region_id
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
        print("FAILED - subquery approach")
        
except Exception as e:
    print(f"Exception: {e}")
