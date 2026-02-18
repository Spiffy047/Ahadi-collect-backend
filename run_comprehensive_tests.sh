#!/bin/bash

# Collections System - Comprehensive Test Suite Runner
# This script runs all test suites to validate the complete system

echo "🚀 COLLECTIONS SYSTEM - COMPREHENSIVE TEST VALIDATION"
echo "============================================================"
echo "This will validate all CRUD operations across all user roles"
echo "and ensure complete frontend-backend integration"
echo "============================================================"

# Check if we're in the backend directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Please run this script from the backend directory"
    echo "   cd backend && ./run_comprehensive_tests.sh"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed"
    exit 1
fi

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import requests, flask, flask_sqlalchemy, flask_jwt_extended, flask_cors" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Error: Required Python packages are missing"
    echo "   Please install: pip install -r requirements.txt"
    exit 1
fi

echo "✅ Dependencies check passed"

# Check if Flask server is running
echo "🔍 Checking Flask server status..."
if curl -s http://localhost:5000/api/regions > /dev/null 2>&1; then
    echo "✅ Flask server is running"
else
    echo "❌ Flask server is not running!"
    echo ""
    echo "Please start the Flask server in another terminal:"
    echo "   cd backend"
    echo "   python app.py"
    echo ""
    echo "Then run this test script again."
    exit 1
fi

# Make test files executable
chmod +x test_comprehensive_crud.py
chmod +x test_frontend_integration.py
chmod +x run_all_tests.py

echo ""
echo "🧪 Starting comprehensive test execution..."
echo "This may take several minutes to complete all test suites."
echo ""

# Run the master test runner
python3 run_all_tests.py

# Capture exit code
TEST_EXIT_CODE=$?

echo ""
echo "📊 Test execution completed!"

if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "🎉 ALL TESTS PASSED! System is fully validated and ready for production."
    echo ""
    echo "✅ Validated Features:"
    echo "   • All CRUD operations for Admin, Manager, and Officer roles"
    echo "   • Complete frontend-backend API integration"
    echo "   • User authentication and role-based permissions"
    echo "   • Payment processing and settlement workflows"
    echo "   • Geo-mapping and location verification"
    echo "   • Reporting and dashboard functionality"
    echo "   • Tag management and batch processing"
    echo "   • Kenyan-specific features (M-Pesa, regions, counties)"
    echo ""
    echo "📝 Detailed test report saved to: test_report.json"
else
    echo "⚠️ Some tests failed. Please review the output above."
    echo "📝 Detailed test report saved to: test_report.json"
fi

echo ""
echo "============================================================"
echo "Test execution completed at $(date)"
echo "============================================================"

exit $TEST_EXIT_CODE