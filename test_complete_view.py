import requests
import json

DRILL_URL = "http://localhost:8047/query.json"

def test_query(query, name):
    print(f"\n{'='*70}")
    print(f"Testing: {name}")
    print(f"{'='*70}")
    
    try:
        payload = {"queryType": "SQL", "query": query}
        response = requests.post(DRILL_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('queryState') == 'COMPLETED':
                rows = data.get('rows', [])
                print(f"✓ SUCCESS - Rows: {len(rows)}")
                if len(rows) > 0:
                    print(f"Sample row: {rows[0]}")
            else:
                print(f"✗ FAILED")
                error_msg = data.get('errorMessage', 'Unknown error')
                print(f"Error: {error_msg[:500]}")  # First 500 chars
        else:
            print(f"✗ HTTP {response.status_code}")
            
    except Exception as e:
        print(f"✗ EXCEPTION: {e}")

if __name__ == "__main__":
    # Test the current "Complete Environmental View" query from sample queries
    current_query = """
        WITH 
        pg_region AS (SELECT region_id, region_name FROM postgres.public.`region_info`),
        pg_climate AS (SELECT region_id, temperature, rainfall FROM postgres.public.`climate_data`),
        pg_agri AS (SELECT region_id, crop_type, yield FROM postgres.public.`agriculture_data`),
        mongo_bio AS (SELECT region_id, species_count FROM mongo.environmental_db.`Biodiversity_Data`),
        csv_sensors AS (SELECT CAST(region_id AS INT) as rid, CAST(co2_level AS FLOAT) as co2, CAST(pm2_5 AS FLOAT) as pm FROM dfs.data.`sensor_readings.csv`)
        SELECT 
            r.region_name,
            c.temperature,
            c.rainfall,
            a.crop_type,
            a.yield,
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
    test_query(current_query, "Complete Environmental View (Current)")
    
    # Test simpler version - just regions
    test_query("""
        SELECT region_id, region_name 
        FROM postgres.public.`region_info` 
        ORDER BY region_id
    """, "All Regions")
    
    # Test CSV data availability
    test_query("""
        SELECT DISTINCT CAST(region_id AS INT) as rid
        FROM dfs.data.`sensor_readings.csv`
        ORDER BY rid
    """, "CSV Region IDs")
