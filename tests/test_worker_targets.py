#!/usr/bin/env python3
"""
Test script for Worker Targets functionality
"""
import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def test_worker_targets():
    """Test the worker targets API endpoints"""
    
    print("🧪 Testing Worker Targets API")
    print("=" * 50)
    
    # Test authentication first (assuming test user exists)
    print("1. Testing authentication...")
    auth_data = {
        "username": "testuser",
        "password": "testpass"
    }
    
    try:
        # Login
        auth_response = requests.post(f"{BASE_URL}/auth/login", data=auth_data)
        if auth_response.status_code == 200:
            token = auth_response.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            print("✅ Authentication successful")
        else:
            print("❌ Authentication failed - you may need to create a test user")
            print("   Run the backend and create a user first")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - is the backend running?")
        print("   Start the backend with: poetry run uvicorn apps.api.main:app --reload")
        return
    
    # Test getting workers with targets
    print("\n2. Testing GET /workers-with-targets...")
    try:
        response = requests.get(f"{BASE_URL}/workers-with-targets", headers=headers)
        if response.status_code == 200:
            workers = response.json()
            print(f"✅ Retrieved {len(workers)} workers")
            if workers:
                print(f"   Sample worker: {workers[0]}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test getting all worker targets
    print("\n3. Testing GET /worker-targets...")
    try:
        response = requests.get(f"{BASE_URL}/worker-targets", headers=headers)
        if response.status_code == 200:
            targets = response.json()
            print(f"✅ Retrieved {len(targets)} worker targets")
            if targets:
                print(f"   Sample target: {targets[0]}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test creating a worker target (if we have workers)
    print("\n4. Testing POST /worker-targets...")
    try:
        # First get available workers
        workers_response = requests.get(f"{BASE_URL}/workers", headers=headers)
        if workers_response.status_code == 200:
            workers = workers_response.json()
            if workers:
                test_worker_id = workers[0]["id"]
                test_target_data = {
                    "id_worker": test_worker_id,
                    "target": 100
                }
                
                create_response = requests.post(f"{BASE_URL}/worker-targets", 
                                              json=test_target_data, headers=headers)
                if create_response.status_code == 200:
                    print(f"✅ Created worker target for worker {test_worker_id}")
                elif create_response.status_code == 400:
                    print(f"ℹ️  Worker target already exists for worker {test_worker_id}")
                else:
                    print(f"❌ Failed: {create_response.status_code} - {create_response.text}")
            else:
                print("ℹ️  No workers available to test target creation")
        else:
            print(f"❌ Could not get workers: {workers_response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Worker Targets API testing completed!")
    print("💡 Access the frontend at: http://localhost:3000/worker-targets")

if __name__ == "__main__":
    test_worker_targets()
