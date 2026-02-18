import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000/api'
token = None

def test_auth():
    global token
    print("🔐 Testing Authentication...")
    
    # Test login
    response = requests.post(f'{BASE_URL}/auth/login', json={
        'username': 'admin',
        'password': 'admin123'
    })
    
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            token = data['data']['token']
            print("✅ Login successful")
            return True
    
    print("❌ Login failed")
    return False

def get_headers():
    return {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

def test_users():
    print("\n👥 Testing User Management...")
    
    # Get users
    response = requests.get(f'{BASE_URL}/users', headers=get_headers())
    if response.status_code == 200 and response.json()['success']:
        users = response.json()['data']
        print(f"✅ Retrieved {len(users)} users")
    else:
        print("❌ Failed to get users")
        return False
    
    # Create user
    new_user = {
        'username': 'test_officer',
        'email': 'test@collections.co.ke',
        'password': 'test123',
        'role': 'collections_officer',
        'regionId': 'REG-001'
    }
    
    response = requests.post(f'{BASE_URL}/users', json=new_user, headers=get_headers())
    if response.status_code == 200 and response.json()['success']:
        print("✅ User created successfully")
    else:
        print("❌ Failed to create user")
        return False
    
    return True

def test_regions():
    print("\n🗺️ Testing Regions...")
    
    response = requests.get(f'{BASE_URL}/regions', headers=get_headers())
    if response.status_code == 200 and response.json()['success']:
        regions = response.json()['data']
        print(f"✅ Retrieved {len(regions)} regions")
        return True
    else:
        print("❌ Failed to get regions")
        return False

def test_consumers():
    print("\n👤 Testing Consumer Management...")
    
    # Get consumers
    response = requests.get(f'{BASE_URL}/consumers', headers=get_headers())
    if response.status_code == 200 and response.json()['success']:
        consumers = response.json()['data']['data']
        print(f"✅ Retrieved {len(consumers)} consumers")
    else:
        print("❌ Failed to get consumers")
        return False
    
    # Create consumer
    new_consumer = {
        'firstName': 'Test',
        'lastName': 'Consumer',
        'phone': '+254 700 123 456',
        'email': 'test.consumer@example.com',
        'addressStreet': '123 Test Street',
        'addressCity': 'Nairobi',
        'addressCounty': 'Nairobi',
        'latitude': -1.2921,
        'longitude': 36.8219,
        'regionId': 'REG-001'
    }
    
    response = requests.post(f'{BASE_URL}/consumers', json=new_consumer, headers=get_headers())
    if response.status_code == 200 and response.json()['success']:
        consumer_id = response.json()['data']['id']
        print("✅ Consumer created successfully")
        
        # Test location verification
        response = requests.put(f'{BASE_URL}/consumers/{consumer_id}/location', 
                              json={'latitude': -1.2921, 'longitude': 36.8219}, 
                              headers=get_headers())
        if response.status_code == 200:
            print("✅ Location verified successfully")
        else:
            print("❌ Failed to verify location")
            
    else:
        print("❌ Failed to create consumer")
        return False
    
    return True

def test_accounts():
    print("\n💳 Testing Account Management...")
    
    # Get accounts
    response = requests.get(f'{BASE_URL}/accounts', headers=get_headers())
    if response.status_code == 200 and response.json()['success']:
        accounts = response.json()['data']['data']
        print(f"✅ Retrieved {len(accounts)} accounts")
        
        if accounts:
            # Test account assignment
            account_id = accounts[0]['id']
            response = requests.put(f'{BASE_URL}/accounts/{account_id}/assign',
                                  json={'officerId': 'USR-003'},
                                  headers=get_headers())
            if response.status_code == 200:
                print("✅ Account assigned successfully")
            else:
                print("❌ Failed to assign account")
        
    else:
        print("❌ Failed to get accounts")
        return False
    
    return True

def test_payments():
    print("\n💰 Testing Payment Processing...")
    
    # Create payment
    payment_data = {
        'accountId': 'ACC-001',
        'amount': 5000.00,
        'paymentMethod': 'mpesa',
        'referenceNumber': 'TEST123456'
    }
    
    response = requests.post(f'{BASE_URL}/payments', json=payment_data, headers=get_headers())
    if response.status_code == 200 and response.json()['success']:
        print("✅ Payment created successfully")
    else:
        print("❌ Failed to create payment")
        return False
    
    return True

def test_tags():
    print("\n🏷️ Testing Tag Management...")
    
    # Get tags
    response = requests.get(f'{BASE_URL}/tags', headers=get_headers())
    if response.status_code == 200 and response.json()['success']:
        tags = response.json()['data']
        print(f"✅ Retrieved {len(tags)} tags")
    else:
        print("❌ Failed to get tags")
        return False
    
    # Create tag
    new_tag = {
        'name': 'Test Tag',
        'category': 'consumer',
        'color': '#ff0000'
    }
    
    response = requests.post(f'{BASE_URL}/tags', json=new_tag, headers=get_headers())
    if response.status_code == 200 and response.json()['success']:
        tag_id = response.json()['data']['id']
        print("✅ Tag created successfully")
        
        # Test tag assignment
        response = requests.post(f'{BASE_URL}/consumers/CON-001/tags',
                               json={'tagId': tag_id},
                               headers=get_headers())
        if response.status_code == 200:
            print("✅ Tag assigned successfully")
        else:
            print("❌ Failed to assign tag")
            
    else:
        print("❌ Failed to create tag")
        return False
    
    return True

def test_jobs():
    print("\n⚙️ Testing Job Management...")
    
    # Get jobs
    response = requests.get(f'{BASE_URL}/jobs', headers=get_headers())
    if response.status_code == 200 and response.json()['success']:
        jobs = response.json()['data']
        print(f"✅ Retrieved {len(jobs)} jobs")
        
        if jobs:
            # Test job execution
            job_id = jobs[0]['id']
            response = requests.post(f'{BASE_URL}/jobs/{job_id}/execute', headers=get_headers())
            if response.status_code == 200:
                print("✅ Job executed successfully")
            else:
                print("❌ Failed to execute job")
        
    else:
        print("❌ Failed to get jobs")
        return False
    
    return True

def test_udd():
    print("\n📊 Testing User-Defined Data...")
    
    # Get UDD tables
    response = requests.get(f'{BASE_URL}/udd/tables', headers=get_headers())
    if response.status_code == 200 and response.json()['success']:
        tables = response.json()['data']
        print(f"✅ Retrieved {len(tables)} UDD tables")
    else:
        print("❌ Failed to get UDD tables")
        return False
    
    # Create UDD table
    new_table = {
        'tableName': 'test_table',
        'fields': [
            {'name': 'field1', 'type': 'string', 'required': True},
            {'name': 'field2', 'type': 'number', 'required': False}
        ]
    }
    
    response = requests.post(f'{BASE_URL}/udd/tables', json=new_table, headers=get_headers())
    if response.status_code == 200 and response.json()['success']:
        print("✅ UDD table created successfully")
        
        # Create UDD record
        record_data = {
            'data': {
                'field1': 'test value',
                'field2': 123
            }
        }
        
        response = requests.post(f'{BASE_URL}/udd/test_table/records', 
                               json=record_data, headers=get_headers())
        if response.status_code == 200:
            print("✅ UDD record created successfully")
        else:
            print("❌ Failed to create UDD record")
            
    else:
        print("❌ Failed to create UDD table")
        return False
    
    return True

def test_geo_mapping():
    print("\n🗺️ Testing Geo Mapping...")
    
    # Get heatmap data
    response = requests.get(f'{BASE_URL}/consumers/heatmap', headers=get_headers())
    if response.status_code == 200 and response.json()['success']:
        heatmap_data = response.json()['data']
        print(f"✅ Retrieved heatmap data for {len(heatmap_data)} consumers")
    else:
        print("❌ Failed to get heatmap data")
        return False
    
    return True

def test_dashboard():
    print("\n📊 Testing Dashboard...")
    
    response = requests.get(f'{BASE_URL}/reports/dashboard', headers=get_headers())
    if response.status_code == 200 and response.json()['success']:
        dashboard_data = response.json()['data']
        print(f"✅ Dashboard data retrieved - {dashboard_data['totalAccounts']} accounts, KSh {dashboard_data['totalBalance']:,.2f} total balance")
    else:
        print("❌ Failed to get dashboard data")
        return False
    
    return True

def run_full_test():
    print("🚀 Starting Full System Functionality Test")
    print("=" * 50)
    
    tests = [
        test_auth,
        test_users,
        test_regions,
        test_consumers,
        test_accounts,
        test_payments,
        test_tags,
        test_jobs,
        test_udd,
        test_geo_mapping,
        test_dashboard
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test failed with error: {e}")
            failed += 1
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! System is fully functional.")
    else:
        print("⚠️ Some tests failed. Check the backend server.")

if __name__ == '__main__':
    run_full_test()