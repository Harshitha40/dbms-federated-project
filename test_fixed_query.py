import requests

DRILL_URL = "http://localhost:8047/query.json"

# Test with yield properly quoted
query = """
WITH 
pg_region AS (SELECT region_id, region_name FROM postgres.public.`region_info`),
pg_climate AS (SELECT region_id, temperature, rainfall FROM postgres.public.`climate_data`),
pg_agri AS (SELECT region_id, crop_type, `yield` as crop_yield FROM postgres.public.`agriculture_data`),
mongo_bio AS (SELECT region_id, species_count FROM mongo.environmental_db.`Biodiversity_Data`),
csv_sensors AS (SELECT CAST(region_id AS INT) as rid, CAST(co2_level AS FLOAT) as co2, CAST(pm2_5 AS FLOAT) as pm FROM dfs.data.`sensor_readings.csv`)
SELECT 
    r.region_name,
    c.temperature,
    c.rainfall,
    a.crop_type,
    a.crop_yield,
    b.species_count,
    s.co2 as co2_level,
    s.pm as pm2_5
FROM pg_region r
LEFT JOIN pg_climate c ON r.region_id = c.region_id
LEFT JOIN pg_agri a ON r.region_id = a.region_id
LEFT JOIN mongo_bio b ON r.region_id = b.region_id
LEFT JOIN csv_sensors s ON s.rid = r.region_id
LIMIT 15
"""

try:
    response = requests.post(DRILL_URL, json={"queryType": "SQL", "query": query}, timeout=30)
    data = response.json()
    
    print(f"Query State: {data.get('queryState')}")
    
    if data.get('queryState') == 'COMPLETED':
        rows = data.get('rows', [])
        print(f"✓ SUCCESS - {len(rows)} rows returned")
        print(f"\nFirst 3 rows:")
        for i, row in enumerate(rows[:3]):
            print(f"{i+1}. {row}")
    else:
        print(f"✗ FAILED")
        # Try to extract error message
        if 'errorMessage' in data:
            print(f"Error: {data['errorMessage']}")
        
except Exception as e:
    print(f"Exception: {e}")
