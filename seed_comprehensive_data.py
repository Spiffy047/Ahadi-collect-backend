#!/usr/bin/env python3
"""
MASTER DATABASE SEEDING SCRIPT - 200+ Consumers
Creates comprehensive test data for Collections Management System
"""

from app import app, db
from models import *
import uuid
from datetime import datetime, date, timedelta
import random
import json
from decimal import Decimal

def seed_comprehensive_data():
    with app.app_context():
        print("🌱 Starting comprehensive database seeding (200+ consumers)...")
        
        db.drop_all()
        db.create_all()
        
        # Regions
        regions = [
            {'id': str(uuid.uuid4()), 'name': 'Nairobi Region', 'code': 'NRB', 'counties': '["Nairobi"]'},
            {'id': str(uuid.uuid4()), 'name': 'Central Region', 'code': 'CNT', 'counties': '["Kiambu","Nyeri"]'},
            {'id': str(uuid.uuid4()), 'name': 'Coast Region', 'code': 'CST', 'counties': '["Mombasa","Kilifi"]'},
            {'id': str(uuid.uuid4()), 'name': 'Western Region', 'code': 'WST', 'counties': '["Kakamega"]'},
            {'id': str(uuid.uuid4()), 'name': 'Rift Valley Region', 'code': 'RVT', 'counties': '["Nakuru","Eldoret"]'}
        ]
        for r in regions:
            db.session.add(Region(**r))
        
        # Users
        users_data = [
            # Administrators
            {'username': 'testsprite', 'email': 'testsprite@collections.com', 'password': 'testsprite', 'role': 'administrator', 'region_id': None},
            {'username': 'admin', 'email': 'admin@collections.com', 'password': 'admin123', 'role': 'administrator', 'region_id': None},
            {'username': 'gm', 'email': 'gm@collections.com', 'password': 'gm123', 'role': 'general_manager', 'region_id': None},
            
            # Managers - one per region
            {'username': 'mgr_nairobi', 'email': 'manager@collections.com', 'password': 'manager123', 'role': 'collections_manager', 'region_id': regions[0]['id']},
            {'username': 'mgr_central', 'email': 'mgr.central@collections.com', 'password': 'manager123', 'role': 'collections_manager', 'region_id': regions[1]['id']},
            {'username': 'mgr_coast', 'email': 'mgr.coast@collections.com', 'password': 'manager123', 'role': 'collections_manager', 'region_id': regions[2]['id']},
            {'username': 'mgr_western', 'email': 'mgr.western@collections.com', 'password': 'manager123', 'role': 'collections_manager', 'region_id': regions[3]['id']},
            {'username': 'mgr_rift', 'email': 'mgr.rift@collections.com', 'password': 'manager123', 'role': 'collections_manager', 'region_id': regions[4]['id']},
            
            # Officers - multiple per region
            # Nairobi: 3 officers
            {'username': 'off_nairobi1', 'email': 'officer@collections.com', 'password': 'officer123', 'role': 'collections_officer', 'region_id': regions[0]['id']},
            {'username': 'off_nairobi2', 'email': 'off2@collections.com', 'password': 'officer123', 'role': 'collections_officer', 'region_id': regions[0]['id']},
            {'username': 'off_nairobi3', 'email': 'off.nairobi3@collections.com', 'password': 'officer123', 'role': 'collections_officer', 'region_id': regions[0]['id']},
            
            # Central: 3 officers
            {'username': 'off_central1', 'email': 'off.central@collections.com', 'password': 'officer123', 'role': 'collections_officer', 'region_id': regions[1]['id']},
            {'username': 'off_central2', 'email': 'off.central2@collections.com', 'password': 'officer123', 'role': 'collections_officer', 'region_id': regions[1]['id']},
            {'username': 'off_central3', 'email': 'off.central3@collections.com', 'password': 'officer123', 'role': 'collections_officer', 'region_id': regions[1]['id']},
            
            # Coast: 3 officers
            {'username': 'off_coast1', 'email': 'off.coast@collections.com', 'password': 'officer123', 'role': 'collections_officer', 'region_id': regions[2]['id']},
            {'username': 'off_coast2', 'email': 'off.coast2@collections.com', 'password': 'officer123', 'role': 'collections_officer', 'region_id': regions[2]['id']},
            {'username': 'off_coast3', 'email': 'off.coast3@collections.com', 'password': 'officer123', 'role': 'collections_officer', 'region_id': regions[2]['id']},
            
            # Western: 2 officers
            {'username': 'off_western1', 'email': 'off.western@collections.com', 'password': 'officer123', 'role': 'collections_officer', 'region_id': regions[3]['id']},
            {'username': 'off_western2', 'email': 'off.western2@collections.com', 'password': 'officer123', 'role': 'collections_officer', 'region_id': regions[3]['id']},
            
            # Rift Valley: 3 officers
            {'username': 'off_rift1', 'email': 'off.rift@collections.com', 'password': 'officer123', 'role': 'collections_officer', 'region_id': regions[4]['id']},
            {'username': 'off_rift2', 'email': 'off.rift2@collections.com', 'password': 'officer123', 'role': 'collections_officer', 'region_id': regions[4]['id']},
            {'username': 'off_rift3', 'email': 'off.rift3@collections.com', 'password': 'officer123', 'role': 'collections_officer', 'region_id': regions[4]['id']},
        ]
        
        users = []
        for u in users_data:
            pwd = u.pop('password')
            user = User(id=str(uuid.uuid4()), **u, active=True)
            user.set_password(pwd)
            users.append(user)
            db.session.add(user)
        
        # Creditors
        creditors = []
        for name, rate in [('ABC Bank', 25), ('KCB', 30), ('Equity', 28), ('Co-op', 27), ('NCBA', 26)]:
            c = Creditor(id=str(uuid.uuid4()), short_name=name, full_name=f'{name} Limited', 
                        contact_email=f'debt@{name.lower().replace(" ","")}.com', 
                        contact_phone=f'+25470{random.randint(1000000,9999999)}', commission_rate=rate, active=True)
            creditors.append(c)
            db.session.add(c)
        
        db.session.commit()
        print(f"✅ Created {len(users)} users, {len(creditors)} creditors, {len(regions)} regions")
        
        # 220 Consumers
        first_names = ['John','Mary','Peter','Grace','David','Sarah','James','Lucy','Michael','Jane','Samuel','Ruth',
                      'Daniel','Faith','Joseph','Esther','Robert','Agnes','Francis','Catherine','Paul','Margaret',
                      'Stephen','Joyce','Anthony','Rose','Charles','Beatrice','George','Alice','Vincent','Mercy',
                      'Patrick','Ann','Thomas','Elizabeth','William','Nancy','Richard','Christine','Andrew','Monica',
                      'Kenneth','Susan','Brian','Dorothy','Kevin','Helen','Dennis','Patricia','Eric','Rebecca']
        
        last_names = ['Kamau','Wanjiku','Omondi','Akinyi','Mwangi','Njeri','Kiprotich','Wambui','Mutua','Moraa',
                     'Kipchoge','Chebet','Otieno','Nyambura','Maina','Wanjiru','Karanja','Muthoni','Mbugua','Wangari',
                     'Macharia','Wairimu','Kiptoo','Adhiambo','Wekesa','Auma','Mutiso','Kemunto','Ochieng','Wanjala']
        
        locations = [
            {"city": "Nairobi", "lat": -1.2921, "lng": 36.8219, "county": "Nairobi", "region_id": regions[0]['id']},
            {"city": "Kiambu", "lat": -1.1748, "lng": 36.8356, "county": "Kiambu", "region_id": regions[1]['id']},
            {"city": "Nyeri", "lat": -0.4167, "lng": 36.9500, "county": "Nyeri", "region_id": regions[1]['id']},
            {"city": "Mombasa", "lat": -4.0435, "lng": 39.6682, "county": "Mombasa", "region_id": regions[2]['id']},
            {"city": "Kilifi", "lat": -3.6309, "lng": 39.8499, "county": "Kilifi", "region_id": regions[2]['id']},
            {"city": "Kakamega", "lat": 0.2827, "lng": 34.7519, "county": "Kakamega", "region_id": regions[3]['id']},
            {"city": "Nakuru", "lat": -0.3031, "lng": 36.0800, "county": "Nakuru", "region_id": regions[4]['id']},
            {"city": "Eldoret", "lat": 0.5143, "lng": 35.2698, "county": "Uasin Gishu", "region_id": regions[4]['id']}
        ]
        
        consumers = []
        print("\n📊 Creating 220 consumers...")
        for i in range(220):
            loc = random.choice(locations)
            consumer = Consumer(
                id=str(uuid.uuid4()),
                first_name=random.choice(first_names),
                last_name=random.choice(last_names),
                national_id=f"{random.randint(10000000,99999999)}",
                phone=f"+25470{random.randint(1000000,9999999)}",
                email=f"consumer{i+1}@example.com",
                address_street=f"{random.randint(1,999)} {random.choice(['Kenyatta','Uhuru','Moi'])} St",
                address_city=loc["city"],
                address_county=loc["county"],
                latitude=loc["lat"] + random.uniform(-0.1, 0.1),
                longitude=loc["lng"] + random.uniform(-0.1, 0.1),
                location_verified=random.choice([True, False]),
                region_id=loc["region_id"]
            )
            consumers.append(consumer)
            db.session.add(consumer)
        
        db.session.commit()
        print(f"✅ Created {len(consumers)} consumers")
        
        # Accounts
        officers = [u for u in users if u.role == 'collections_officer']
        # Create officer lookup by region
        officers_by_region = {}
        for officer in officers:
            if officer.region_id not in officers_by_region:
                officers_by_region[officer.region_id] = []
            officers_by_region[officer.region_id].append(officer)
        
        accounts = []
        statuses = ['active', 'active', 'active', 'active', 'paid_in_full', 'settled', 'closed']
        
        print("\n💳 Creating accounts...")
        for i, consumer in enumerate(consumers):
            # Get officers in the same region as consumer
            region_officers = officers_by_region.get(consumer.region_id, officers)
            if not region_officers:
                region_officers = officers  # Fallback to any officer if no regional officer
            
            for j in range(random.choices([1, 2, 3], weights=[60, 30, 10])[0]):
                original = random.randint(10000, 1000000)
                status = random.choice(statuses)
                current = original * random.uniform(0.2, 1.0) if status == 'active' else 0
                
                account = Account(
                    id=str(uuid.uuid4()),
                    consumer_id=consumer.id,
                    creditor_id=random.choice(creditors).id,
                    account_number=f"ACC-{i+1:04d}-{j+1}",
                    original_balance=original,
                    current_balance=current,
                    principal_balance=current * 0.7,
                    interest_balance=current * 0.2,
                    fee_balance=current * 0.1,
                    status=status,
                    placement_date=date.today() - timedelta(days=random.randint(30, 730)),
                    assigned_officer_id=random.choice(region_officers).id
                )
                accounts.append(account)
                db.session.add(account)
        
        db.session.commit()
        print(f"✅ Created {len(accounts)} accounts")
        
        # Payments
        print("\n💰 Creating payments...")
        payment_count = 0
        for account in random.sample(accounts, min(300, len(accounts))):
            if account.status in ['active', 'paid_in_full', 'settled']:
                for _ in range(random.randint(1, 5)):
                    payment = Payment(
                        id=str(uuid.uuid4()),
                        account_id=account.id,
                        amount=random.randint(5000, 100000),
                        payment_method=random.choice(['mpesa', 'bank_transfer', 'cash', 'cheque']),
                        status='completed',
                        processed_date=datetime.now() - timedelta(days=random.randint(0, 365)),
                        reference_number=f"REF{random.randint(100000,999999)}",
                        created_by=account.assigned_officer_id,
                        created_at=datetime.now() - timedelta(days=random.randint(0, 365))
                    )
                    db.session.add(payment)
                    payment_count += 1
        
        db.session.commit()
        print(f"✅ Created {payment_count} payments")
        
        # PTPs
        print("\n🤝 Creating PTPs...")
        ptp_count = 0
        for account in random.sample(accounts, min(250, len(accounts))):
            if account.status == 'active':
                for _ in range(random.randint(1, 4)):
                    ptp = PromiseToPay(
                        id=str(uuid.uuid4()),
                        account_id=account.id,
                        consumer_id=account.consumer_id,
                        promised_amount=random.randint(5000, 100000),
                        promised_date=date.today() + timedelta(days=random.randint(-60, 60)),
                        payment_method=random.choice(['mpesa', 'bank_transfer', 'cash']),
                        contact_method=random.choice(['phone_call', 'sms', 'email', 'whatsapp']),
                        consumer_response=random.choice(['PTP', 'LMES', 'cooperative', 'hostile']),
                        follow_up_action=random.choice(['call_back', 'field_visit', 'escalate']),
                        status=random.choice(['active', 'kept', 'broken', 'cancelled']),
                        notes=f"PTP recorded",
                        created_by=account.assigned_officer_id,
                        created_at=datetime.now() - timedelta(days=random.randint(0, 90))
                    )
                    db.session.add(ptp)
                    ptp_count += 1
        
        db.session.commit()
        print(f"✅ Created {ptp_count} PTPs")
        
        # Legal Cases
        print("\n⚖️ Creating legal cases...")
        legal_count = 0
        firms = ['Kamau & Associates', 'Wanjiku Legal', 'Omondi Law Firm', 'Akinyi Advocates']
        for account in random.sample(accounts, min(80, len(accounts))):
            case_type = random.choice(['court_case', 'demand_letter', 'arbitration', 'repossession'])
            status = random.choice(['pending', 'in_progress', 'settled', 'dismissed'])
            filed = date.today() - timedelta(days=random.randint(30, 730))
            
            legal = LegalCase(
                id=str(uuid.uuid4()),
                account_id=account.id,
                case_number=f"LC-{date.today().year}-{legal_count+1:04d}",
                case_type=case_type,
                status=status,
                filed_date=filed,
                resolution_date=filed + timedelta(days=random.randint(30, 365)) if status == 'settled' else None,
                recovery_amount=random.randint(50000, 500000) if status == 'settled' else 0,
                legal_costs=random.randint(10000, 100000),
                assigned_firm=random.choice(firms),
                notes=f"Legal case",
                created_by=random.choice([u.id for u in users if u.role in ['collections_manager', 'general_manager']])
            )
            db.session.add(legal)
            legal_count += 1
        
        db.session.commit()
        print(f"✅ Created {legal_count} legal cases")
        
        # AR Events
        print("\n📝 Creating AR events...")
        event_count = 0
        for account in random.sample(accounts, min(200, len(accounts))):
            for _ in range(random.randint(2, 8)):
                event = AREvent(
                    id=str(uuid.uuid4()),
                    account_id=account.id,
                    event_type=random.choice(['contact', 'payment', 'promise', 'dispute', 'visit']),
                    description=f"Event for {account.account_number}",
                    created_by=account.assigned_officer_id,
                    created_at=datetime.now() - timedelta(days=random.randint(0, 180))
                )
                db.session.add(event)
                event_count += 1
        
        db.session.commit()
        print(f"✅ Created {event_count} AR events")
        
        # Settlements - Create for ALL active accounts
        print("\n💼 Creating settlements...")
        settlement_count = 0
        active_accounts = [a for a in accounts if a.status == 'active']
        for account in active_accounts:
            # Each active account gets a settlement offer
            discount = Decimal(str(random.uniform(20, 60)))
            settlement = Settlement(
                id=str(uuid.uuid4()),
                account_id=account.id,
                original_balance=account.current_balance,
                settlement_amount=account.current_balance * (Decimal('1') - discount/Decimal('100')),
                discount_percentage=discount,
                status=random.choice(['proposed', 'approved', 'rejected', 'completed']),
                proposed_date=datetime.now() - timedelta(days=random.randint(0, 90)),
                notes=f"Settlement offer {float(discount):.1f}% discount",
                created_by=account.assigned_officer_id
            )
            db.session.add(settlement)
            settlement_count += 1
        
        db.session.commit()
        print(f"✅ Created {settlement_count} settlements")
        
        # Payment Schedules - Create for ALL active accounts
        print("\n📅 Creating payment schedules...")
        schedule_count = 0
        active_accounts = [a for a in accounts if a.status == 'active']
        for account in active_accounts:
            # Each active account gets a payment schedule
            freq = random.choice(['weekly', 'monthly', 'quarterly'])
            payment_amt = account.current_balance / random.randint(3, 12)
            schedule = PaymentSchedule(
                id=str(uuid.uuid4()),
                account_id=account.id,
                total_amount=account.current_balance,
                payment_amount=payment_amt,
                frequency=freq,
                start_date=date.today() + timedelta(days=random.randint(1, 30)),
                status=random.choice(['active', 'active', 'completed', 'cancelled']),
                created_by=account.assigned_officer_id,
                created_at=datetime.now() - timedelta(days=random.randint(0, 60))
            )
            db.session.add(schedule)
            schedule_count += 1
        
        db.session.commit()
        print(f"✅ Created {schedule_count} payment schedules")
        
        # Service Providers
        print("\n🚗 Creating service providers...")
        providers_data = [
            {'name': 'QuickRepo Services', 'type': 'vehicle_repossession', 'person': 'John Kamau', 'phone': '+254701234567', 'areas': '["Nairobi","Kiambu"]', 'rating': 4.5, 'lat': -1.2921, 'lng': 36.8219},
            {'name': 'Asset Valuers Ltd', 'type': 'property_valuation', 'person': 'Mary Wanjiku', 'phone': '+254702345678', 'areas': '["Nairobi","Nyeri"]', 'rating': 4.2, 'lat': -1.2850, 'lng': 36.8200},
            {'name': 'Legal Eagles', 'type': 'legal_services', 'person': 'Peter Omondi', 'phone': '+254703456789', 'areas': '["Mombasa","Kilifi"]', 'rating': 4.8, 'lat': -4.0435, 'lng': 39.6682},
            {'name': 'Recovery Masters', 'type': 'asset_recovery', 'person': 'Grace Akinyi', 'phone': '+254704567890', 'areas': '["Nakuru","Eldoret"]', 'rating': 4.3, 'lat': -0.3031, 'lng': 36.0800},
            {'name': 'Debt Solutions Kenya', 'type': 'debt_collection', 'person': 'David Mwangi', 'phone': '+254705678901', 'areas': '["Kakamega"]', 'rating': 4.0, 'lat': 0.2827, 'lng': 34.7519}
        ]
        providers = []
        for p in providers_data:
            provider = ServiceProvider(
                id=str(uuid.uuid4()),
                name=p['name'],
                service_type=p['type'],
                contact_person=p['person'],
                phone=p['phone'],
                email=f"{p['name'].lower().replace(' ', '')}@example.com",
                latitude=p['lat'],
                longitude=p['lng'],
                coverage_areas=p['areas'],
                rating=p['rating'],
                active=True
            )
            providers.append(provider)
            db.session.add(provider)
        
        db.session.commit()
        print(f"✅ Created {len(providers)} service providers")
        
        # Collateral Assets - Create for ALL accounts (not just sample)
        print("\n🏠 Creating collateral assets...")
        asset_count = 0
        for account in accounts:
            # Each account gets 1-2 collateral assets
            num_assets = random.randint(1, 2)
            for _ in range(num_assets):
                loc = random.choice(locations)
                asset_type = random.choice(['land', 'motor_vehicle', 'property', 'machinery'])
                asset = CollateralAsset(
                    id=str(uuid.uuid4()),
                    account_id=account.id,
                    asset_type=asset_type,
                    description=f"{asset_type.replace('_', ' ').title()} - {account.account_number}",
                    estimated_value=random.randint(500000, 5000000),
                    current_status=random.choice(['available', 'repossessed', 'under_valuation', 'disputed']),
                    location_address=f"{random.randint(1,999)} {random.choice(['Mombasa','Thika','Nakuru'])} Road, {loc['city']}",
                    latitude=loc['lat'] + random.uniform(-0.05, 0.05),
                    longitude=loc['lng'] + random.uniform(-0.05, 0.05),
                    assigned_provider_id=random.choice(providers).id if random.random() > 0.3 else None,
                    registration_number=f"KCA-{random.randint(100,999)}{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}" if asset_type == 'motor_vehicle' else None
                )
                db.session.add(asset)
                asset_count += 1
        
        db.session.commit()
        print(f"✅ Created {asset_count} collateral assets")
        
        # External Receivers
        print("\n📤 Creating external receivers...")
        receivers_data = [
            {'name': 'Kamau & Associates Law Firm', 'type': 'law_firm', 'person': 'James Kamau', 'phone': '+254706789012', 'commission': 15, 'success': 65, 'lat': -1.2800, 'lng': 36.8150},
            {'name': 'Debt Recovery Experts', 'type': 'debt_collector', 'person': 'Lucy Njeri', 'phone': '+254707890123', 'commission': 20, 'success': 58, 'lat': -1.2950, 'lng': 36.8250},
            {'name': 'Asset Auctioneers Ltd', 'type': 'auction_house', 'person': 'Michael Kiprotich', 'phone': '+254708901234', 'commission': 10, 'success': 72, 'lat': -4.0500, 'lng': 39.6700},
            {'name': 'Recovery Agents Kenya', 'type': 'recovery_agent', 'person': 'Jane Wambui', 'phone': '+254709012345', 'commission': 18, 'success': 61, 'lat': -0.3100, 'lng': 36.0850}
        ]
        receivers = []
        for r in receivers_data:
            receiver = ExternalReceiver(
                id=str(uuid.uuid4()),
                name=r['name'],
                receiver_type=r['type'],
                contact_person=r['person'],
                phone=r['phone'],
                email=f"{r['name'].lower().replace(' ', '').replace('&','and')}@example.com",
                latitude=r['lat'],
                longitude=r['lng'],
                commission_rate=r['commission'],
                success_rate=r['success'],
                coverage_areas='["Nairobi","Mombasa","Nakuru"]',
                active=True
            )
            receivers.append(receiver)
            db.session.add(receiver)
        
        db.session.commit()
        print(f"✅ Created {len(receivers)} external receivers")
        
        # Tags
        print("\n🏷️ Creating tags...")
        tags_data = [
            {'name': 'High Priority', 'category': 'account', 'color': '#FF0000'},
            {'name': 'VIP Customer', 'category': 'consumer', 'color': '#FFD700'},
            {'name': 'Legal Action', 'category': 'account', 'color': '#8B0000'},
            {'name': 'Payment Plan', 'category': 'account', 'color': '#00FF00'},
            {'name': 'Disputed', 'category': 'account', 'color': '#FFA500'},
            {'name': 'Cooperative', 'category': 'consumer', 'color': '#0000FF'},
            {'name': 'Hard to Reach', 'category': 'consumer', 'color': '#808080'},
            {'name': 'Settlement Candidate', 'category': 'account', 'color': '#800080'}
        ]
        tags = []
        for t in tags_data:
            tag = Tag(
                id=str(uuid.uuid4()),
                name=t['name'],
                category=t['category'],
                color=t['color'],
                active=True
            )
            tags.append(tag)
            db.session.add(tag)
        
        db.session.commit()
        print(f"✅ Created {len(tags)} tags")
        
        # Alerts - Create for ALL active accounts
        print("\n🔔 Creating alerts...")
        alert_count = 0
        active_accounts = [a for a in accounts if a.status == 'active']
        for account in active_accounts:
            # Each active account gets an alert
            alert_type = random.choice(['payment_due', 'payment_overdue', 'ptp_due', 'ptp_broken', 'high_priority'])
            alert = Alert(
                id=str(uuid.uuid4()),
                alert_type=alert_type,
                title=f"{alert_type.replace('_', ' ').title()} - {account.account_number}",
                message=f"Alert for account {account.account_number}",
                priority=random.choice(['low', 'medium', 'high', 'critical']),
                account_id=account.id,
                consumer_id=account.consumer_id,
                assigned_to=account.assigned_officer_id,
                status=random.choice(['active', 'active', 'acknowledged', 'resolved']),
                due_date=date.today() + timedelta(days=random.randint(-30, 30)),
                created_at=datetime.now() - timedelta(days=random.randint(0, 60))
            )
            db.session.add(alert)
            alert_count += 1
        
        db.session.commit()
        print(f"✅ Created {alert_count} alerts")
        
        # Escalations
        print("\n⬆️ Creating escalations...")
        escalation_count = 0
        managers = [u for u in users if u.role in ['collections_manager', 'general_manager']]
        for account in random.sample([a for a in accounts if a.status == 'active'], min(20, len([a for a in accounts if a.status == 'active']))):
            escalation = Escalation(
                id=str(uuid.uuid4()),
                account_id=account.id,
                escalated_by=account.assigned_officer_id,
                escalated_to=random.choice(managers).id,
                reason=random.choice(['High balance overdue', 'Consumer unresponsive', 'Legal action required', 'Dispute resolution needed']),
                status=random.choice(['pending', 'acknowledged', 'resolved']),
                priority=random.choice(['low', 'medium', 'high', 'urgent']),
                created_at=datetime.now() - timedelta(days=random.randint(0, 45))
            )
            db.session.add(escalation)
            escalation_count += 1
        
        db.session.commit()
        print(f"✅ Created {escalation_count} escalations")
        
        # Summary
        print("\n" + "="*60)
        print("🎉 DATABASE SEEDING COMPLETED!")
        print("="*60)
        print(f"👥 Users: {len(users)}")
        print(f"🏢 Regions: {len(regions)}")
        print(f"🏦 Creditors: {len(creditors)}")
        print(f"👤 Consumers: {len(consumers)}")
        print(f"💳 Accounts: {len(accounts)}")
        print(f"💰 Payments: {payment_count}")
        print(f"🤝 PTPs: {ptp_count}")
        print(f"⚖️ Legal Cases: {legal_count}")
        print(f"📝 AR Events: {event_count}")
        print(f"💼 Settlements: {settlement_count}")
        print(f"📅 Payment Schedules: {schedule_count}")
        print(f"🚗 Service Providers: {len(providers)}")
        print(f"🏠 Collateral Assets: {asset_count}")
        print(f"📤 External Receivers: {len(receivers)}")
        print(f"🏷️ Tags: {len(tags)}")
        print(f"🔔 Alerts: {alert_count}")
        print(f"⬆️ Escalations: {escalation_count}")
        print("="*60)

if __name__ == '__main__':
    seed_comprehensive_data()
