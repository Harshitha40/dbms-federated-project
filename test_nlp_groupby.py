import requests
import json

def test_nlp_groupby(question):
    print(f"\n{'='*60}")
    print(f"Question: {question}")
    print(f"{'='*60}")
    
    try:
        session = requests.Session()
        
        # Login
        login_response = session.post(
            "http://localhost:5000/api/login",
            json={"email": "sarah.researcher@example.com", "password": "password123"}
        )
        
        if login_response.status_code != 200:
            print(f"Login failed")
            return
        
        # Send natural query
        response = session.post(
            "http://localhost:5000/api/natural-query",
            json={"query": question},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✓ Success: {data.get('success')}")
            print(f"Generated SQL:\n{data.get('generated_sql')}\n")
            print(f"Confidence: {data.get('confidence')}")
            
            if data.get('success'):
                print(f"Rows returned: {len(data.get('data', []))}")
            else:
                print(f"Error: {data.get('error')}")
        else:
            print(f"✗ HTTP {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"✗ Exception: {e}")

if __name__ == "__main__":
    # Test GROUP BY queries
    test_nlp_groupby("What is the average temperature by region?")
    test_nlp_groupby("Show me regions with average temperature above 20 degrees")
    test_nlp_groupby("Count the number of crops by region")
