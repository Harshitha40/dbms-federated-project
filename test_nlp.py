import requests
import json

API_URL = "http://localhost:5000/api/natural-query"

def test_nlp_query(question):
    print(f"\n--- Testing NLP Query ---")
    print(f"Question: {question}")
    
    try:
        # Create a session to handle cookies
        session = requests.Session()
        
        # First login
        login_response = session.post(
            "http://localhost:5000/api/login",
            json={
                "email": "sarah.researcher@example.com",
                "password": "password123"
            }
        )
        
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code}")
            return
        
        print("Login successful")
        
        # Now send the natural query
        response = session.post(
            API_URL,
            json={"query": question},
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success: {data.get('success')}")
            print(f"Generated SQL: {data.get('generated_sql')}")
            print(f"Interpretation: {data.get('interpretation')}")
            print(f"Confidence: {data.get('confidence')}")
            
            if data.get('success'):
                print(f"Rows returned: {len(data.get('data', []))}")
            else:
                print(f"Error: {data.get('error')}")
        else:
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_nlp_query("Show me all regions")
