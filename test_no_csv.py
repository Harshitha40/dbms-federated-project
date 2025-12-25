import requests

DRILL_URL = "http://localhost:8047/query.json"

# Test: All 3 Postgres tables + Mongo (no CSV)
query = """
WITH 
pg_region AS (SELECT region_id, region_name FROM postgres.public.`region_info`),
pg_climate AS (SELECT region_id, temperature, rainfall FROM postgres.public.`climate_data`),
pg_agri AS (SELECT region_id, crop_type, `yield` as crop_yield FROM postgres.public.`agriculture_data`),
mongo_bio AS (SELECT region_id, species_count FROM mongo.environmental_db.`Biodiversity_Data`)
SELECT 
    r.region_name,
    c.temperature,
    c.rainfall,
    a.crop_type,
    a.crop_yield,
    b.species_count
FROM pg_region r
LEFT JOIN pg_climate c ON r.region_id = c.region_id
LEFT JOIN pg_agri a ON r.region_id = a.region_id
LEFT JOIN mongo_bio b ON r.region_id = b.region_id
LIMIT 15
"""

try:
    response = requests.post(DRILL_URL, json={"queryType": "SQL", "query": query}, timeout=30)
    data = response.json()
    
    if data.get('queryState') == 'COMPLETED':
        rows = data.get('rows', [])
        print(f"SUCCESS! {len(rows)} rows - Postgres (3 tables) + Mongo works!")
        print("\nFirst 2 rows:")
        for i, row in enumerate(rows[:2]):
            print(f"{i+1}. {row}")
    else:
        print("FAILED - 4 CTEs (3 Postgres + 1 Mongo)")
        
except Exception as e:
    print(f"Exception: {e}")
