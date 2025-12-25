import requests

DRILL_URL = "http://localhost:8047/query.json"

def test(query, name):
    print(f"\n{name}:")
    try:
        response = requests.post(DRILL_URL, json={"queryType": "SQL", "query": query}, timeout=30)
        data = response.json()
        if data.get('queryState') == 'COMPLETED':
            print(f"  SUCCESS - {len(data.get('rows', []))} rows")
            return True
        else:
            print(f"  FAILED")
            return False
    except Exception as e:
        print(f"  ERROR - {str(e)[:80]}")
        return False

# Build up complexity step by step
test("""
WITH pg_region AS (SELECT region_id, region_name FROM postgres.public.`region_info`)
SELECT * FROM pg_region LIMIT 5
""", "Step 1: Single CTE")

test("""
WITH 
pg_region AS (SELECT region_id, region_name FROM postgres.public.`region_info`),
pg_climate AS (SELECT region_id, temperature FROM postgres.public.`climate_data`)
SELECT r.region_name, c.temperature
FROM pg_region r
LEFT JOIN pg_climate c ON r.region_id = c.region_id
LIMIT 5
""", "Step 2: Two Postgres CTEs")

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
""", "Step 3: Three Postgres CTEs (no yield)")

test("""
WITH 
pg_region AS (SELECT region_id, region_name FROM postgres.public.`region_info`),
pg_climate AS (SELECT region_id, temperature FROM postgres.public.`climate_data`),
mongo_bio AS (SELECT region_id, species_count FROM mongo.environmental_db.`Biodiversity_Data`)
SELECT r.region_name, c.temperature, b.species_count
FROM pg_region r
LEFT JOIN pg_climate c ON r.region_id = c.region_id
LEFT JOIN mongo_bio b ON r.region_id = b.region_id
LIMIT 5
""", "Step 4: Postgres + Mongo")

test("""
WITH 
pg_region AS (SELECT region_id, region_name FROM postgres.public.`region_info`),
csv_sensors AS (SELECT CAST(region_id AS INT) as rid, CAST(co2_level AS FLOAT) as co2 FROM dfs.data.`sensor_readings.csv`)
SELECT r.region_name, s.co2
FROM pg_region r
LEFT JOIN csv_sensors s ON s.rid = r.region_id
LIMIT 5
""", "Step 5: Postgres + CSV")

test("""
WITH 
pg_region AS (SELECT region_id, region_name FROM postgres.public.`region_info`),
pg_climate AS (SELECT region_id, temperature FROM postgres.public.`climate_data`),
mongo_bio AS (SELECT region_id, species_count FROM mongo.environmental_db.`Biodiversity_Data`),
csv_sensors AS (SELECT CAST(region_id AS INT) as rid, CAST(co2_level AS FLOAT) as co2 FROM dfs.data.`sensor_readings.csv`)
SELECT r.region_name, c.temperature, b.species_count, s.co2
FROM pg_region r
LEFT JOIN pg_climate c ON r.region_id = c.region_id
LEFT JOIN mongo_bio b ON r.region_id = b.region_id
LEFT JOIN csv_sensors s ON s.rid = r.region_id
LIMIT 5
""", "Step 6: All 4 sources (minimal columns)")
