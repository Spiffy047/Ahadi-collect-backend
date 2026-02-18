#!/bin/bash

# DM9 Collections Backend Setup Script

echo "Setting up DM9 Collections Backend..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file - please update with your settings"
fi

# Initialize and seed database
python db_manager.py reset
python db_manager.py seed

echo "Backend setup complete!"
echo ""
echo "To start the backend:"
echo "1. source venv/bin/activate"
echo "2. python app.py"
echo ""
echo "Database management:"
echo "python db_manager.py status    # Check database status"
echo "python db_manager.py seed     # Reseed data"
echo "python db_manager.py reset    # Reset database"
echo ""
echo "Default login credentials:"
echo "Administrator: admin / admin123"
echo "Manager: manager_nairobi / manager123"
echo "Officer: officer_nairobi1 / officer123"