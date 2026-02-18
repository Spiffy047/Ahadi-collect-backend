from app import app
from models import *
from datetime import datetime, timedelta
import uuid
import json

with app.app_context():
    # Recreate database with new models
    db.create_all()
    
    # Create sample alerts
    accounts = Account.query.limit(5).all()
    users = User.query.filter_by(role='collections_officer').all()
    
    if accounts and users:
        alerts_data = [
            {
                'alert_type': 'payment_overdue',
                'title': 'Payment Overdue - High Priority',
                'message': f'Account {accounts[0].account_number} is 45 days overdue',
                'priority': 'high',
                'account_id': accounts[0].id,
                'assigned_to': users[0].id,
                'due_date': datetime.utcnow().date() - timedelta(days=45)
            },
            {
                'alert_type': 'ptp_broken',
                'title': 'Promise to Pay Broken',
                'message': f'Consumer failed to honor PTP for account {accounts[1].account_number}',
                'priority': 'medium',
                'account_id': accounts[1].id,
                'assigned_to': users[0].id if len(users) == 1 else users[1].id,
                'due_date': datetime.utcnow().date() - timedelta(days=3)
            },
            {
                'alert_type': 'high_priority',
                'title': 'High Value Account - No Contact',
                'message': f'Unable to reach consumer for high-value account {accounts[2].account_number}',
                'priority': 'critical',
                'account_id': accounts[2].id,
                'assigned_to': users[0].id,
                'due_date': datetime.utcnow().date()
            }
        ]
        
        for alert_data in alerts_data:
            alert = Alert(
                id=str(uuid.uuid4()),
                **alert_data
            )
            db.session.add(alert)
    
    # Create service providers
    providers_data = [
        {
            'name': 'Elite Vehicle Recovery Services',
            'service_type': 'vehicle_repossession',
            'contact_person': 'John Kamau',
            'phone': '+254722123456',
            'email': 'info@eliterecovery.co.ke',
            'address': 'Industrial Area, Nairobi',
            'latitude': -1.3197,
            'longitude': 36.8510,
            'rating': 4.5,
            'coverage_areas': json.dumps(['Nairobi', 'Kiambu', 'Machakos'])
        },
        {
            'name': 'Prime Property Valuers',
            'service_type': 'property_valuation',
            'contact_person': 'Mary Wanjiku',
            'phone': '+254733987654',
            'email': 'valuations@primevaluers.co.ke',
            'address': 'Westlands, Nairobi',
            'latitude': -1.2676,
            'longitude': 36.8108,
            'rating': 4.8,
            'coverage_areas': json.dumps(['Nairobi', 'Kiambu', 'Kajiado'])
        },
        {
            'name': 'Coastal Legal Associates',
            'service_type': 'legal_services',
            'contact_person': 'Ahmed Hassan',
            'phone': '+254741555777',
            'email': 'legal@coastallaw.co.ke',
            'address': 'Mombasa CBD',
            'latitude': -4.0435,
            'longitude': 39.6682,
            'rating': 4.2,
            'coverage_areas': json.dumps(['Mombasa', 'Kilifi', 'Kwale'])
        }
    ]
    
    for provider_data in providers_data:
        provider = ServiceProvider(
            id=str(uuid.uuid4()),
            **provider_data
        )
        db.session.add(provider)
    
    # Create collateral assets
    if accounts:
        assets_data = [
            {
                'account_id': accounts[0].id,
                'asset_type': 'motor_vehicle',
                'description': 'Toyota Hilux 2018',
                'estimated_value': 2500000,
                'current_status': 'available',
                'location_address': 'Karen, Nairobi',
                'latitude': -1.3197,
                'longitude': 36.7076,
                'registration_number': 'KCA 123A'
            },
            {
                'account_id': accounts[1].id,
                'asset_type': 'land',
                'description': '2-acre plot in Kiambu',
                'estimated_value': 8000000,
                'current_status': 'under_valuation',
                'location_address': 'Kiambu Town',
                'latitude': -1.1748,
                'longitude': 36.8356,
                'title_deed_number': 'KIAMBU/KIAMBU/1234'
            },
            {
                'account_id': accounts[2].id,
                'asset_type': 'property',
                'description': '3-bedroom house',
                'estimated_value': 12000000,
                'current_status': 'repossessed',
                'location_address': 'Thika Road, Nairobi',
                'latitude': -1.2297,
                'longitude': 36.8756,
                'title_deed_number': 'NAIROBI/BLOCK45/567'
            }
        ]
        
        for asset_data in assets_data:
            asset = CollateralAsset(
                id=str(uuid.uuid4()),
                **asset_data
            )
            db.session.add(asset)
    
    db.session.commit()
    print(f'Added {len(alerts_data)} alerts, {len(providers_data)} service providers, and {len(assets_data)} collateral assets')