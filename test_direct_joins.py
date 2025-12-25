import requests

DRILL_URL = "http://localhost:8047/query.json"

# Approach: Use only 3 CTEs - one per data source (Postgres, Mongo, CSV)
# But Postgres has 3 tables, so we need to pre-join them somehow...
# Actually, let's try direct joins for same-database tables

query = """
SELECT 
    r.region_name,
    c.temperature,
    c.rainfall,
    a.crop_type,
    a.`yield` as crop_yield,
    b.species_count,
    CAST(s.co2_level AS FLOAT) as co2_level,
    CAST(s.pm2_5 AS FLOAT) as pm2_5
FROM postgres.public.`region_info` r
LEFT JOIN postgres.public.`climate_data` c ON r.region_id = c.region_id
LEFT JOIN postgres.public.`agriculture_data` a ON r.region_id = a.region_id
LEFT JOIN mongo.environmental_db.`Biodiversity_Data` b ON r.region_id = b.region_id
LEFT JOIN dfs.data.`sensor_readings.csv` s ON CAST(s.region_id AS INT) = r.region_id
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
        print("FAILED - trying direct joins without CTEs")
        
except Exception as e:
    print(f"Exception: {e}")
