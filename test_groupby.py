import requests
import json

DRILL_URL = "http://localhost:8047/query.json"

def run_query(query, name):
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print(f"{'='*60}")
    print(f"Query:\n{query}\n")
    
    try:
        payload = {"queryType": "SQL", "query": query}
        response = requests.post(DRILL_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('queryState') == 'COMPLETED':
                rows = data.get('rows', [])
                print(f"✓ SUCCESS - Rows: {len(rows)}")
                if rows and len(rows) <= 3:
                    for row in rows:
                        print(f"  {row}")
            else:
                print(f"✗ FAILED")
                print(f"Error: {data.get('errorMessage', 'Unknown error')}")
        else:
            print(f"✗ HTTP {response.status_code}")
            
    except Exception as e:
        print(f"✗ EXCEPTION: {e}")

if __name__ == "__main__":
    # Test 1: Simple GROUP BY with CTE
    run_query("""
        WITH pg_climate AS (
            SELECT region_id, temperature 
            FROM postgres.public.`climate_data`
        )
        SELECT region_id, AVG(temperature) as avg_temp
        FROM pg_climate
        GROUP BY region_id
        LIMIT 5
    """, "GROUP BY with CTE")
    
    # Test 2: GROUP BY without CTE (direct)
    run_query("""
        SELECT region_id, AVG(temperature) as avg_temp
        FROM postgres.public.`climate_data`
        GROUP BY region_id
        LIMIT 5
    """, "Direct GROUP BY")
    
    # Test 3: GROUP BY with JOIN and CTE
    run_query("""
        WITH 
        pg_region AS (SELECT region_id, region_name FROM postgres.public.`region_info`),
        pg_climate AS (SELECT region_id, temperature FROM postgres.public.`climate_data`)
        SELECT r.region_name, AVG(c.temperature) as avg_temp
        FROM pg_region r
        JOIN pg_climate c ON r.region_id = c.region_id
        GROUP BY r.region_name
        LIMIT 5
    """, "GROUP BY with CTE JOIN")
    
    # Test 4: Nested query (subquery in FROM)
    run_query("""
        SELECT region_name, avg_temp
        FROM (
            SELECT r.region_name, AVG(c.temperature) as avg_temp
            FROM postgres.public.`region_info` r
            JOIN postgres.public.`climate_data` c ON r.region_id = c.region_id
            GROUP BY r.region_name
        ) subq
        WHERE avg_temp > 20
        LIMIT 5
    """, "Nested Query with WHERE")
    
    # Test 5: GROUP BY with HAVING
    run_query("""
        WITH 
        pg_region AS (SELECT region_id, region_name FROM postgres.public.`region_info`),
        pg_climate AS (SELECT region_id, temperature FROM postgres.public.`climate_data`)
        SELECT r.region_name, AVG(c.temperature) as avg_temp
        FROM pg_region r
        JOIN pg_climate c ON r.region_id = c.region_id
        GROUP BY r.region_name
        HAVING AVG(c.temperature) > 20
        LIMIT 5
    """, "GROUP BY with HAVING")
