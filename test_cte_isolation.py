import requests

DRILL_URL = "http://localhost:8047/query.json"

def test(query, name):
    print(f"\n{name}:")
    try:
        response = requests.post(DRILL_URL, json={"queryType": "SQL", "query": query}, timeout=30)
        data = response.json()
        if data.get('queryState') == 'COMPLETED':
            print(f"  ✓ SUCCESS - {len(data.get('rows', []))} rows")
        else:
            print(f"  ✗ FAILED - {data.get('errorMessage', 'No error msg')[:100]}")
    except Exception as e:
        print(f"  ✗ EXCEPTION: {str(e)[:100]}")

# Test each CTE individually
test("SELECT region_id, region_name FROM postgres.public.`region_info` LIMIT 5", "1. Postgres Regions")
test("SELECT region_id, temperature, rainfall FROM postgres.public.`climate_data` LIMIT 5", "2. Postgres Climate")
test("SELECT region_id, crop_type, yield FROM postgres.public.`agriculture_data` LIMIT 5", "3. Postgres Agriculture")
test("SELECT region_id, species_count FROM mongo.environmental_db.`Biodiversity_Data` LIMIT 5", "4. Mongo Biodiversity")
test("SELECT CAST(region_id AS INT) as rid, CAST(co2_level AS FLOAT) as co2 FROM dfs.data.`sensor_readings.csv` LIMIT 5", "5. CSV Sensors")

# Test simple 2-table CTE join
test("""
WITH 
pg_region AS (SELECT region_id, region_name FROM postgres.public.`region_info`),
pg_climate AS (SELECT region_id, temperature FROM postgres.public.`climate_data`)
SELECT r.region_name, c.temperature
FROM pg_region r
JOIN pg_climate c ON r.region_id = c.region_id
LIMIT 5
""", "6. Simple 2-table CTE")

# Test 3-table CTE join
test("""
WITH 
pg_region AS (SELECT region_id, region_name FROM postgres.public.`region_info`),
pg_climate AS (SELECT region_id, temperature FROM postgres.public.`climate_data`),
pg_agri AS (SELECT region_id, crop_type FROM postgres.public.`agriculture_data`)
SELECT r.region_name, c.temperature, a.crop_type
FROM pg_region r
LEFT JOIN pg_climate c ON r.region_id = c.region_id
LEFT JOIN pg_agri a ON r.region_id = a.region_id
LIMIT 5
""", "7. Three Postgres tables")
