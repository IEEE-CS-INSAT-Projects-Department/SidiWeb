"""
Quick test for Flask API using requests library.
Tests all endpoints without needing Postman.
"""
import requests
import json
import time

BASE_URL = "http://localhost:5001"

def print_header(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_root():
    print_header("TEST 1: Root Endpoint (GET /)")
    
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_health():
    print_header("TEST 2: Health Check (GET /health)")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_recommend_valid():
    print_header("TEST 3: Valid Recommendation (POST /recommend)")
    
    data = {
        "category": "startup",
        "style": "moderne",
        "preferences": "tech, innovant"
    }
    
    try:
        print(f"Request:\n{json.dumps(data, indent=2)}")
        response = requests.post(
            f"{BASE_URL}/recommend",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"\nStatus: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_recommend_invalid():
    print_header("TEST 4: Invalid Request (Missing Fields)")
    
    data = {
        "category": "startup"
    }
    
    try:
        print(f"Request:\n{json.dumps(data, indent=2)}")
        response = requests.post(
            f"{BASE_URL}/recommend",
            json=data,
            headers={"Content-Type": "application/json"}
        )
        print(f"\nStatus: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        return response.status_code == 422
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_recommend_no_body():
    print_header("TEST 5: No JSON Body")
    
    try:
        response = requests.post(
            f"{BASE_URL}/recommend",
            headers={"Content-Type": "application/json"}
        )
        print(f"Status: {response.status_code}")
        
        try:
            print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response:\n{response.text}")
        
        return response.status_code in [400, 415]
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "=" * 70)
    print("  FLASK API TEST SUITE")
    print("  Make sure Flask server is running on port 5001")
    print("=" * 70)
    
    time.sleep(1)
    
    results = []
    
    results.append(("Root endpoint", test_root()))
    time.sleep(0.5)
    
    results.append(("Health check", test_health()))
    time.sleep(0.5)
    
    results.append(("Valid recommendation", test_recommend_valid()))
    time.sleep(2)
    
    results.append(("Invalid request", test_recommend_invalid()))
    time.sleep(0.5)
    
    results.append(("No JSON body", test_recommend_no_body()))
    
    print_header("TEST RESULTS")
    passed = 0
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {name}")
        if result:
            passed += 1
    
    print(f"\n{passed}/{len(results)} tests passed")
    print("=" * 70)

if __name__ == "__main__":
    main()
