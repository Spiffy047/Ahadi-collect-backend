#!/usr/bin/env python3
"""Validate consumer region assignments and officer account assignments"""

from app import app, db
from models import Consumer, Account, User, Region
from collections import defaultdict

with app.app_context():
    print("=" * 80)
    print("CONSUMER & ACCOUNT ASSIGNMENT VALIDATION")
    print("=" * 80)
    
    # Get all regions
    regions = Region.query.all()
    
    for region in regions:
        print(f"\n{'='*80}")
        print(f"REGION: {region.name} ({region.code})")
        print(f"{'='*80}")
        
        # Get consumers in this region
        consumers = Consumer.query.filter_by(region_id=region.id).all()
        print(f"\n📊 Consumers in region: {len(consumers)}")
        
        # Get officers in this region
        officers = User.query.filter_by(role='collections_officer', region_id=region.id).all()
        print(f"👮 Officers in region: {len(officers)}")
        for officer in officers:
            print(f"   - {officer.username} ({officer.email})")
        
        # Get accounts for consumers in this region
        consumer_ids = [c.id for c in consumers]
        accounts_in_region = Account.query.filter(Account.consumer_id.in_(consumer_ids)).all() if consumer_ids else []
        print(f"\n💳 Total accounts for region consumers: {len(accounts_in_region)}")
        
        # Check officer assignments
        officer_account_counts = defaultdict(int)
        misassigned_accounts = []
        
        for account in accounts_in_region:
            officer_account_counts[account.assigned_officer_id] += 1
            
            # Check if officer is in the same region as consumer
            officer = User.query.get(account.assigned_officer_id)
            consumer = Consumer.query.get(account.consumer_id)
            
            if officer and consumer:
                if officer.region_id != consumer.region_id:
                    misassigned_accounts.append({
                        'account': account.account_number,
                        'consumer': f"{consumer.first_name} {consumer.last_name}",
                        'consumer_region': consumer.region_id,
                        'officer': officer.username,
                        'officer_region': officer.region_id
                    })
        
        print(f"\n📈 Accounts per officer:")
        for officer in officers:
            count = officer_account_counts.get(officer.id, 0)
            print(f"   - {officer.username}: {count} accounts")
        
        # Check for accounts assigned to officers from other regions
        other_region_officers = set(officer_account_counts.keys()) - set(o.id for o in officers)
        if other_region_officers:
            print(f"\n⚠️  WARNING: {len(other_region_officers)} accounts assigned to officers from OTHER regions!")
            for officer_id in other_region_officers:
                officer = User.query.get(officer_id)
                count = officer_account_counts[officer_id]
                if officer:
                    print(f"   - {officer.username} (from {officer.region.name if officer.region else 'No Region'}): {count} accounts")
        
        if misassigned_accounts:
            print(f"\n❌ MISASSIGNED ACCOUNTS: {len(misassigned_accounts)}")
            for ma in misassigned_accounts[:5]:  # Show first 5
                print(f"   - Account {ma['account']}: Consumer in one region, Officer in another")
    
    # Summary
    print(f"\n{'='*80}")
    print("SUMMARY")
    print(f"{'='*80}")
    
    total_consumers = Consumer.query.count()
    total_accounts = Account.query.count()
    total_officers = User.query.filter_by(role='collections_officer').count()
    
    print(f"Total Consumers: {total_consumers}")
    print(f"Total Accounts: {total_accounts}")
    print(f"Total Officers: {total_officers}")
    
    # Check for any accounts with NULL officer assignment
    null_officer_accounts = Account.query.filter_by(assigned_officer_id=None).count()
    if null_officer_accounts > 0:
        print(f"\n⚠️  WARNING: {null_officer_accounts} accounts have NO officer assigned!")
    
    # Check overall misassignment
    all_misassigned = 0
    for account in Account.query.all():
        officer = User.query.get(account.assigned_officer_id)
        consumer = Consumer.query.get(account.consumer_id)
        if officer and consumer and officer.region_id != consumer.region_id:
            all_misassigned += 1
    
    if all_misassigned > 0:
        print(f"\n❌ TOTAL MISASSIGNED: {all_misassigned} accounts assigned to officers outside consumer's region")
        print(f"   This means accounts are randomly assigned, not region-based!")
    else:
        print(f"\n✅ ALL ACCOUNTS CORRECTLY ASSIGNED: Officers match consumer regions")
