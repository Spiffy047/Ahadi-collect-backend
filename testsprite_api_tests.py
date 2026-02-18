#!/usr/bin/env python3
"""
TestSprite API Tests for Collections Backend
Tests all critical API endpoints
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class TestSpriteAPITests:
    def __init__(self):
        self.api_key = os.getenv('TESTSPRITE_API_KEY')
        self.base_url = "http://localhost:5000/api"
        self.token = None
        
    def login(self):
        """Login and get JWT token"""
        response = requests.post(
            f"{self.base_url}/auth/login",
            json={
                "email": "testsprite@collections.com",
                "password": "testsprite"
            }
        )
        if response.status_code == 200:
            self.token = response.json().get('access_token')
            return True
        return False
    
    def get_headers(self):
        """Get authorization headers"""
        return {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    def test_accounts_list(self):
        """Test GET /api/accounts"""
        print("Testing: GET /api/accounts")
        response = requests.get(
            f"{self.base_url}/accounts?page=1&per_page=10",
            headers=self.get_headers()
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert 'accounts' in data, "Response missing 'accounts' key"
        print(f"✅ Accounts list: {len(data['accounts'])} accounts found")
        return True
    
    def test_consumers_list(self):
        """Test GET /api/consumers"""
        print("Testing: GET /api/consumers")
        response = requests.get(
            f"{self.base_url}/consumers?page=1&per_page=10",
            headers=self.get_headers()
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        assert 'consumers' in data, "Response missing 'consumers' key"
        print(f"✅ Consumers list: {len(data['consumers'])} consumers found")
        return True
    
    def test_analytics_dashboard(self):
        """Test GET /api/analytics/dashboard"""
        print("Testing: GET /api/analytics/dashboard")
        response = requests.get(
            f"{self.base_url}/analytics/collections-trend",
            headers=self.get_headers()
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        print(f"✅ Collections trend data retrieved")
        return True
    
    def test_legal_cases(self):
        """Test GET /api/analytics/legal-cases"""
        print("Testing: GET /api/analytics/legal-cases")
        response = requests.get(
            f"{self.base_url}/analytics/legal-cases?period=30",
            headers=self.get_headers()
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        data = response.json()
        print(f"✅ Legal cases: {data.get('court_cases', 0)} court cases, {data.get('handovers', 0)} handovers")
        return True
    
    def test_create_payment(self):
        """Test POST /api/payments"""
        print("Testing: POST /api/payments")
        
        # Get first account
        accounts_response = requests.get(
            f"{self.base_url}/accounts?page=1&per_page=10",
            headers=self.get_headers()
        )
        accounts = accounts_response.json().get('accounts', [])
        
        if not accounts:
            print("⚠️ No accounts available for payment test")
            return True
        
        account_id = accounts[0]['id']
        
        response = requests.post(
            f"{self.base_url}/payments",
            headers=self.get_headers(),
            json={
                "account_id": account_id,
                "amount": 5000,
                "payment_method": "mpesa",
                "reference_number": "TEST123"
            }
        )
        assert response.status_code in [200, 201], f"Expected 200/201, got {response.status_code}"
        print(f"✅ Payment created successfully")
        return True
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🧪 Starting TestSprite API Tests\n")
        
        if not self.login():
            print("❌ Login failed")
            return False
        
        print("✅ Login successful\n")
        
        tests = [
            self.test_accounts_list,
            self.test_consumers_list,
            self.test_analytics_dashboard,
            self.test_legal_cases,
            self.test_create_payment
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                test()
                passed += 1
            except AssertionError as e:
                print(f"❌ Test failed: {str(e)}")
                failed += 1
            except Exception as e:
                print(f"❌ Test error: {str(e)}")
                failed += 1
            print()
        
        print(f"\n{'='*50}")
        print(f"Test Results: {passed} passed, {failed} failed")
        print(f"{'='*50}")
        
        return failed == 0

if __name__ == '__main__':
    tester = TestSpriteAPITests()
    success = tester.run_all_tests()
    exit(0 if success else 1)
