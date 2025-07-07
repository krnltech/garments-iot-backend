#!/usr/bin/env python3
"""
Backend API Testing Script
Run this script to test if your modular backend is working properly.
"""
import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8001"
API_BASE = f"{BASE_URL}/api/v1"

class BackendTester:
    def __init__(self):
        self.session = requests.Session()
        self.token = None
        self.user_data = None
    
    def print_test_result(self, test_name: str, success: bool, message: str = ""):
        """Print formatted test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if message:
            print(f"    {message}")
        print()
    
    def test_health_check(self):
        """Test health check endpoint"""
        try:
            response = self.session.get(f"{BASE_URL}/health")
            success = response.status_code == 200
            data = response.json() if success else None
            message = f"Status: {response.status_code}, Response: {data}"
            self.print_test_result("Health Check", success, message)
            return success
        except Exception as e:
            self.print_test_result("Health Check", False, f"Error: {str(e)}")
            return False
    
    def test_user_registration(self):
        """Test user registration"""
        try:
            user_data = {
                "username": f"testuser_{int(datetime.now().timestamp())}",
                "email": f"test_{int(datetime.now().timestamp())}@example.com",
                "full_name": "Test User",
                "password": "testpassword123"
            }
            
            response = self.session.post(f"{API_BASE}/auth/register", json=user_data)
            success = response.status_code == 200
            
            if success:
                self.user_data = user_data
                response_data = response.json()
                message = f"Created user: {response_data['username']} (ID: {response_data['id']})"
            else:
                try:
                    error_detail = response.json().get('detail', 'Unknown error')
                except:
                    error_detail = response.text
                message = f"Status: {response.status_code}, Error: {error_detail}"
            
            self.print_test_result("User Registration", success, message)
            return success
        except Exception as e:
            self.print_test_result("User Registration", False, f"Error: {str(e)}")
            return False
    
    def test_user_login(self):
        """Test user login"""
        if not self.user_data:
            self.print_test_result("User Login", False, "No user data available for login test")
            return False
        
        try:
            login_data = {
                "username": self.user_data["username"],
                "password": self.user_data["password"]
            }
            
            response = self.session.post(
                f"{API_BASE}/auth/login",
                data=login_data,  # OAuth2PasswordRequestForm expects form data
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            success = response.status_code == 200
            
            if success:
                response_data = response.json()
                self.token = response_data["access_token"]
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                message = f"Login successful, token obtained"
            else:
                try:
                    error_detail = response.json().get('detail', 'Unknown error')
                except:
                    error_detail = response.text
                message = f"Status: {response.status_code}, Error: {error_detail}"
            
            self.print_test_result("User Login", success, message)
            return success
        except Exception as e:
            self.print_test_result("User Login", False, f"Error: {str(e)}")
            return False
    
    def test_protected_endpoint(self):
        """Test accessing protected endpoint"""
        if not self.token:
            self.print_test_result("Protected Endpoint", False, "No authentication token available")
            return False
        
        try:
            response = self.session.get(f"{API_BASE}/auth/me")
            success = response.status_code == 200
            
            if success:
                user_info = response.json()
                message = f"User info retrieved: {user_info['full_name']} ({user_info['username']})"
            else:
                try:
                    error_detail = response.json().get('detail', 'Unknown error')
                except:
                    error_detail = response.text
                message = f"Status: {response.status_code}, Error: {error_detail}"
            
            self.print_test_result("Protected Endpoint (/auth/me)", success, message)
            return success
        except Exception as e:
            self.print_test_result("Protected Endpoint", False, f"Error: {str(e)}")
            return False
    
    def test_dashboard_data(self):
        """Test dashboard summary endpoint"""
        if not self.token:
            self.print_test_result("Dashboard Data", False, "No authentication token available")
            return False
        
        try:
            response = self.session.get(f"{API_BASE}/dashboard/summary")
            success = response.status_code == 200
            
            if success:
                dashboard_data = response.json()
                message = f"Dashboard data: Bundles: {dashboard_data['total_bundles_today']}, Machines: {dashboard_data['total_machines']}, Workers: {dashboard_data['total_workers']}"
            else:
                try:
                    error_detail = response.json().get('detail', 'Unknown error')
                except:
                    error_detail = response.text
                message = f"Status: {response.status_code}, Error: {error_detail}"
            
            self.print_test_result("Dashboard Data", success, message)
            return success
        except Exception as e:
            self.print_test_result("Dashboard Data", False, f"Error: {str(e)}")
            return False
    
    def test_machines_endpoint(self):
        """Test machines endpoint"""
        if not self.token:
            self.print_test_result("Machines Endpoint", False, "No authentication token available")
            return False
        
        try:
            response = self.session.get(f"{API_BASE}/machines")
            success = response.status_code == 200
            
            if success:
                machines = response.json()
                message = f"Retrieved {len(machines)} machines"
            else:
                try:
                    error_detail = response.json().get('detail', 'Unknown error')
                except:
                    error_detail = response.text
                message = f"Status: {response.status_code}, Error: {error_detail}"
            
            self.print_test_result("Machines Endpoint", success, message)
            return success
        except Exception as e:
            self.print_test_result("Machines Endpoint", False, f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("🧪 Testing Modular Backend API")
        print("=" * 50)
        print()
        
        tests = [
            self.test_health_check,
            self.test_user_registration,
            self.test_user_login,
            self.test_protected_endpoint,
            self.test_dashboard_data,
            self.test_machines_endpoint
        ]
        
        passed = 0
        total = len(tests)
        
        for test in tests:
            if test():
                passed += 1
        
        print("=" * 50)
        print(f"Tests completed: {passed}/{total} passed")
        
        if passed == total:
            print("🎉 All tests passed! Your modular backend is working correctly.")
            return True
        else:
            print("⚠️  Some tests failed. Check the errors above.")
            return False

def main():
    """Main function"""
    print("Starting Backend API Tests...")
    print(f"Testing against: {BASE_URL}")
    print()
    
    tester = BackendTester()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
