#!/usr/bin/env python3
"""
Add more officers per region to ensure proper manager-officer hierarchy
"""

from app import app, db
from models import User, Region, Account, Payment, PromiseToPay, AREvent
import uuid
from datetime import datetime, timedelta
import random

def add_more_officers():
    """Add more officers to each region"""
    
    with app.app_context():
        print("👥 Adding more officers per region...")
        
        # Get existing regions
        regions = Region.query.all()
        
        # Additional officers data
        additional_officers = [
            # Nairobi Region officers
            {'username': 'officer_nairobi3', 'email': 'officer3.nairobi@collections.com', 'region_name': 'Nairobi Region'},
            {'username': 'officer_nairobi4', 'email': 'officer4.nairobi@collections.com', 'region_name': 'Nairobi Region'},
            {'username': 'officer_nairobi5', 'email': 'officer5.nairobi@collections.com', 'region_name': 'Nairobi Region'},
            
            # Central Region officers
            {'username': 'officer_central2', 'email': 'officer2.central@collections.com', 'region_name': 'Central Region'},
            {'username': 'officer_central3', 'email': 'officer3.central@collections.com', 'region_name': 'Central Region'},
            {'username': 'officer_central4', 'email': 'officer4.central@collections.com', 'region_name': 'Central Region'},
            
            # Coast Region officers (new region needs officers)
            {'username': 'officer_coast1', 'email': 'officer1.coast@collections.com', 'region_name': 'Coast Region'},
            {'username': 'officer_coast2', 'email': 'officer2.coast@collections.com', 'region_name': 'Coast Region'},
            {'username': 'officer_coast3', 'email': 'officer3.coast@collections.com', 'region_name': 'Coast Region'},
        ]
        
        # Create region mapping
        region_map = {r.name: r.id for r in regions}
        
        new_officers = []
        for officer_data in additional_officers:
            region_id = region_map.get(officer_data['region_name'])
            if region_id:
                user = User(
                    id=str(uuid.uuid4()),
                    username=officer_data['username'],
                    email=officer_data['email'],
                    role='collections_officer',
                    region_id=region_id,
                    active=True
                )
                user.set_password('officer123')
                new_officers.append(user)
                db.session.add(user)
        
        db.session.commit()
        
        # Assign some existing accounts to new officers
        unassigned_accounts = Account.query.filter_by(assigned_officer_id=None).all()
        all_officers = User.query.filter_by(role='collections_officer').all()
        
        for account in unassigned_accounts[:20]:  # Assign first 20 unassigned accounts
            account.assigned_officer_id = random.choice(all_officers).id
        
        # Create additional performance data for new officers
        for officer in new_officers:
            # Create some payments
            officer_accounts = Account.query.filter_by(assigned_officer_id=officer.id).all()
            if officer_accounts:
                for _ in range(random.randint(5, 15)):
                    account = random.choice(officer_accounts)
                    payment = Payment(
                        id=str(uuid.uuid4()),
                        account_id=account.id,
                        amount=random.randint(1000, 50000),
                        payment_method=random.choice(['mpesa', 'bank_transfer', 'cash']),
                        status='completed',
                        processed_date=datetime.now() - timedelta(days=random.randint(0, 90)),
                        reference_number=f"REF{random.randint(100000, 999999)}",
                        created_by=officer.id,
                        created_at=datetime.now() - timedelta(days=random.randint(0, 90))
                    )
                    db.session.add(payment)
                
                # Create PTPs
                for _ in range(random.randint(3, 8)):
                    account = random.choice(officer_accounts)
                    ptp = PromiseToPay(
                        id=str(uuid.uuid4()),
                        account_id=account.id,
                        consumer_id=account.consumer_id,
                        promised_amount=random.randint(5000, 100000),
                        promised_date=datetime.now().date() + timedelta(days=random.randint(-30, 30)),
                        payment_method=random.choice(['mpesa', 'bank_transfer', 'cash']),
                        status=random.choice(['active', 'kept', 'broken']),
                        notes=f"PTP created by {officer.username}",
                        created_by=officer.id,
                        created_at=datetime.now() - timedelta(days=random.randint(0, 60))
                    )
                    db.session.add(ptp)
                
                # Create AR Events
                for _ in range(random.randint(10, 25)):
                    account = random.choice(officer_accounts)
                    event = AREvent(
                        id=str(uuid.uuid4()),
                        account_id=account.id,
                        event_type=random.choice(['contact', 'payment', 'visit', 'dispute']),
                        description=f"Activity logged by {officer.username}",
                        created_by=officer.id,
                        created_at=datetime.now() - timedelta(days=random.randint(0, 90))
                    )
                    db.session.add(event)
        
        db.session.commit()
        
        # Add a Coast Region manager
        coast_region = Region.query.filter_by(name='Coast Region').first()
        if coast_region:
            coast_manager = User(
                id=str(uuid.uuid4()),
                username='manager_coast',
                email='manager.coast@collections.com',
                role='collections_manager',
                region_id=coast_region.id,
                active=True
            )
            coast_manager.set_password('manager123')
            db.session.add(coast_manager)
            db.session.commit()
        
        print("✅ Officers added successfully!")
        
        # Show the hierarchy
        for region in regions:
            managers = User.query.filter_by(role='collections_manager', region_id=region.id).all()
            officers = User.query.filter_by(role='collections_officer', region_id=region.id).all()
            
            print(f"\n📍 {region.name}:")
            for manager in managers:
                print(f"   👔 Manager: {manager.username} ({manager.email})")
            print(f"   👥 Officers ({len(officers)}):")
            for officer in officers:
                print(f"      - {officer.username} ({officer.email})")

if __name__ == '__main__':
    add_more_officers()