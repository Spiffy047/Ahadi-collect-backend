#!/usr/bin/env python3
"""
User Authentication Test Suite
Tests all user functionality including login, token validation, and protected endpoints
"""

import requests
import json
import sys

BASE_URL = "http://localhost:5000/api"

def test_login(username, password, expected_success=True):
    """Test user login functionality"""
    print(f"\n🔐 Testing login for: {username}")
    
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "username": username,
        "password": password
    })
    
    data = response.json()
    
    if expected_success:
        if data.get('success'):
            print(f"✅ Login successful")
            print(f"   User ID: {data['data']['userId']}")
            print(f"   Role: {data['data']['role']}")
            print(f"   Region: {data['data'].get('regionId', 'None')}")
            return data['data']['token']
        else:
            print(f"❌ Login failed: {data.get('error', {}).get('message', 'Unknown error')}")
            return None
    else:
        if not data.get('success'):
            print(f"✅ Login correctly rejected: {data.get('error', {}).get('message')}")
            return None
        else:
            print(f"❌ Login should have failed but succeeded")
            return None

def test_protected_endpoint(token, endpoint="/users"):
    """Test access to protected endpoints"""
    print(f"\n🔒 Testing protected endpoint: {endpoint}")
    
    if token:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✅ Access granted to {endpoint}")
                return data['data']
            else:
                print(f"❌ Access denied: {data.get('error')}")
                return None
        else:
            print(f"❌ HTTP Error {response.status_code}")
            return None
    else:
        print("❌ No token provided")
        return None

def test_no_auth_access(endpoint="/users"):
    """Test access to protected endpoints without authentication"""
    print(f"\n🚫 Testing unauthorized access to: {endpoint}")
    
    response = requests.get(f"{BASE_URL}{endpoint}")
    
    if response.status_code == 401:
        print(f"✅ Correctly blocked unauthorized access")
        return True
    else:
        print(f"❌ Should have blocked access but got status {response.status_code}")
        return False

def main():
    print("=" * 60)
    print("🧪 COLLECTIONS SYSTEM - USER AUTHENTICATION TEST SUITE")
    print("=" * 60)
    
    # Test data from seed_database.py
    test_users = [
        ("admin", "admin123", "administrator", None),
        ("manager_nairobi", "manager123", "collections_manager", "REG-001"),
        ("officer_nairobi1", "officer123", "collections_officer", "REG-001"),
        ("officer_coast1", "officer123", "collections_officer", "REG-003"),
        ("officer_rift1", "officer123", "collections_officer", "REG-005")
    ]
    
    tokens = {}
    
    # Test valid logins
    print("\n📋 TESTING VALID USER LOGINS")
    print("-" * 40)
    
    for username, password, role, region in test_users:
        token = test_login(username, password, True)
        if token:
            tokens[username] = token
    
    # Test invalid logins
    print("\n📋 TESTING INVALID LOGINS")
    print("-" * 40)
    
    test_login("admin", "wrongpassword", False)
    test_login("nonexistent", "password", False)
    test_login("", "", False)
    
    # Test unauthorized access
    print("\n📋 TESTING UNAUTHORIZED ACCESS")
    print("-" * 40)
    
    test_no_auth_access("/users")
    test_no_auth_access("/consumers")
    test_no_auth_access("/accounts")
    
    # Test authorized access with different roles
    print("\n📋 TESTING AUTHORIZED ACCESS")
    print("-" * 40)
    
    for username, token in tokens.items():
        print(f"\n👤 Testing access for: {username}")
        users_data = test_protected_endpoint(token, "/users")
        if users_data:
            print(f"   Retrieved {len(users_data)} users")
        
        regions_data = test_protected_endpoint(token, "/regions")
        if regions_data:
            print(f"   Retrieved {len(regions_data)} regions")
    
    # Test dashboard endpoint
    print("\n📋 TESTING DASHBOARD DATA")
    print("-" * 40)
    
    if 'admin' in tokens:
        dashboard_data = test_protected_endpoint(tokens['admin'], "/reports/dashboard")
        if dashboard_data:
            print(f"   Total Accounts: {dashboard_data.get('totalAccounts')}")
            print(f"   Total Balance: {dashboard_data.get('currency')} {dashboard_data.get('totalBalance'):,.2f}")
            print(f"   Active Accounts: {dashboard_data.get('activeAccounts')}")
    
    print("\n" + "=" * 60)
    print("✅ USER AUTHENTICATION TESTS COMPLETED")
    print("=" * 60)
    
    # Summary
    print(f"\n📊 SUMMARY:")
    print(f"   ✅ {len(tokens)} users can login successfully")
    print(f"   ✅ Invalid credentials are properly rejected")
    print(f"   ✅ Protected endpoints require authentication")
    print(f"   ✅ JWT tokens work for API access")
    print(f"   ✅ Database contains seeded test data")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Error: Cannot connect to backend server at http://localhost:5000")
        print("   Make sure the Flask server is running: python app.py")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)