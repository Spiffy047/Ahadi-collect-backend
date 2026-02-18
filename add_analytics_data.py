#!/usr/bin/env python3
"""Add analytics data to existing database"""

from app import app, db
from models import Account, Payment, PaymentPromise
import uuid
from datetime import datetime, timedelta
import random

with app.app_context():
    print("📊 Adding analytics data...")
    
    accounts = Account.query.all()
    print(f"Found {len(accounts)} accounts")
    
    for account in accounts:
        # Add 2-5 payment promises per account
        for _ in range(random.randint(2, 5)):
            promise = PaymentPromise(
                id=str(uuid.uuid4()),
                account_id=account.id,
                promise_date=(datetime.utcnow() - timedelta(days=random.randint(1, 60))).date(),
                promise_amount=random.randint(5000, 50000),
                status=random.choice(['kept', 'broken', 'pending']),
                notes='Payment promise'
            )
            db.session.add(promise)
        
        # Add 1-3 payments per account
        for _ in range(random.randint(1, 3)):
            payment = Payment(
                id=str(uuid.uuid4()),
                account_id=account.id,
                amount=random.randint(10000, 100000),
                payment_date=(datetime.utcnow() - timedelta(days=random.randint(1, 90))).date(),
                payment_method=random.choice(['mpesa', 'bank_transfer', 'cash']),
                status='completed'
            )
            db.session.add(payment)
    
    db.session.commit()
    print("✅ Analytics data added successfully!")
