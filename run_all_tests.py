#!/usr/bin/env python3
"""
MASTER TEST RUNNER
Executes all comprehensive test suites for the Collections System
Provides complete validation of CRUD operations, frontend integration, and system functionality
"""

import subprocess
import sys
import time
import requests
from datetime import datetime
import json

def check_server_status():
    """Check if the Flask server is running"""
    try:
        response = requests.get('http://localhost:5000/api/regions', timeout=5)
        return True
    except:
        return False

def run_test_suite(test_file, description):
    """Run a test suite and capture results"""
    print(f"\n{'='*80}")
    print(f"🧪 RUNNING: {description}")
    print(f"{'='*80}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, timeout=300)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        success = result.returncode == 0
        return {
            'name': description,
            'file': test_file,
            'success': success,
            'duration': duration,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'return_code': result.returncode
        }
        
    except subprocess.TimeoutExpired:
        print(f"❌ Test suite timed out after 5 minutes")
        return {
            'name': description,
            'file': test_file,
            'success': False,
            'duration': 300,
            'error': 'Timeout after 5 minutes'
        }
    except Exception as e:
        print(f"❌ Error running test suite: {e}")
        return {
            'name': description,
            'file': test_file,
            'success': False,
            'duration': 0,
            'error': str(e)
        }

def generate_test_report(results):
    """Generate a comprehensive test report"""
    report = {
        'timestamp': datetime.now().isoformat(),
        'total_suites': len(results),
        'passed_suites': sum(1 for r in results if r['success']),
        'failed_suites': sum(1 for r in results if not r['success']),
        'total_duration': sum(r.get('duration', 0) for r in results),
        'results': results
    }
    
    # Save detailed report
    with open('test_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    return report

def print_summary_report(report):
    """Print a summary of all test results"""
    print(f"\n{'='*80}")
    print(f"📊 COMPREHENSIVE TEST SUMMARY")
    print(f"{'='*80}")
    print(f"Timestamp: {report['timestamp']}")
    print(f"Total Test Suites: {report['total_suites']}")
    print(f"Passed: {report['passed_suites']}")
    print(f"Failed: {report['failed_suites']}")
    print(f"Total Duration: {report['total_duration']:.2f} seconds")
    print(f"{'='*80}")
    
    print(f"\n📋 DETAILED RESULTS:")
    for result in report['results']:
        status = "✅ PASSED" if result['success'] else "❌ FAILED"
        duration = result.get('duration', 0)
        print(f"  {status} - {result['name']} ({duration:.2f}s)")
        
        if not result['success'] and 'error' in result:
            print(f"    Error: {result['error']}")
    
    print(f"\n{'='*80}")
    
    if report['failed_suites'] == 0:
        print(f"🎉 ALL TEST SUITES PASSED!")
        print(f"✅ System is fully functional and ready for production")
        print(f"✅ All CRUD operations validated across all user roles")
        print(f"✅ Frontend-backend integration confirmed")
        print(f"✅ All endpoints properly secured and accessible")
    else:
        print(f"⚠️ {report['failed_suites']} test suite(s) failed")
        print(f"📝 Review the detailed results above")
        print(f"🔍 Check test_report.json for complete details")
    
    print(f"{'='*80}")

def main():
    """Main test runner function"""
    print("🚀 COLLECTIONS SYSTEM - COMPREHENSIVE TEST SUITE")
    print("=" * 80)
    print("This will run all test suites to validate the complete system:")
    print("  1. Comprehensive CRUD Tests (All roles, All endpoints)")
    print("  2. Frontend Integration Tests (API compatibility)")
    print("  3. System Functionality Tests (End-to-end)")
    print("=" * 80)
    
    # Check if server is running
    print("\n🔍 Checking server status...")
    if not check_server_status():
        print("❌ Flask server is not running!")
        print("Please start the server first:")
        print("  cd backend")
        print("  python app.py")
        return 1
    
    print("✅ Flask server is running")
    
    # Define test suites
    test_suites = [
        {
            'file': 'test_comprehensive_crud.py',
            'description': 'Comprehensive CRUD Tests (All Roles & Endpoints)'
        },
        {
            'file': 'test_frontend_integration.py',
            'description': 'Frontend-Backend Integration Tests'
        },
        {
            'file': 'test_system.py',
            'description': 'System Functionality Tests'
        },
        {
            'file': 'test_frontend_api.py',
            'description': 'Frontend API Compatibility Tests'
        }
    ]
    
    # Run all test suites
    results = []
    for suite in test_suites:
        result = run_test_suite(suite['file'], suite['description'])
        results.append(result)
        
        # Small delay between test suites
        time.sleep(2)
    
    # Generate and display report
    report = generate_test_report(results)
    print_summary_report(report)
    
    # Return appropriate exit code
    return 0 if report['failed_suites'] == 0 else 1

if __name__ == '__main__':
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n❌ Test execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        sys.exit(1)