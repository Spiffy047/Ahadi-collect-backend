#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import db, DemandLetterTemplate, User
from app import app
import uuid
from datetime import datetime

def create_sample_demand_letter_template():
    with app.app_context():
        # Find the general manager
        gm = User.query.filter_by(email='gm@collections.com').first()
        if not gm:
            print("General manager not found. Please run seed_general_manager.py first.")
            return
        
        # Check if template already exists
        existing = DemandLetterTemplate.query.filter_by(name='First Notice - Payment Demand').first()
        if existing:
            print("Sample demand letter template already exists.")
            return
        
        # Create sample demand letter template
        template_content = """Dear {CLIENT_NAME},

RE: OUTSTANDING DEBT - ACCOUNT NUMBER {ACCOUNT_NUMBER}

This letter serves as formal notice that your account shows an outstanding balance of {AMOUNT_DUE} as of {DATE}.

Despite previous attempts to contact you regarding this matter, this amount remains unpaid and is now significantly overdue.

IMMEDIATE ACTION REQUIRED:
You are hereby demanded to pay the full amount of {AMOUNT_DUE} within SEVEN (7) days of receiving this notice.

Failure to respond to this demand may result in:
• Legal action being commenced against you without further notice
• Additional costs, interest charges, and legal fees being added to your account
• Negative impact on your credit rating and creditworthiness
• Referral to external collection agencies or legal counsel

PAYMENT OPTIONS:
To resolve this matter immediately, you may:
1. Pay the full amount of {AMOUNT_DUE} via M-Pesa to Paybill 123456
2. Contact our office at +254-700-123456 to arrange a payment plan
3. Visit our offices during business hours (8:00 AM - 5:00 PM, Monday to Friday)

This is a serious matter that requires your immediate attention. We strongly encourage you to contact us within the specified timeframe to avoid further collection activities.

If you believe this notice is in error or if you have already made payment, please contact us immediately with proof of payment.

Time is of the essence. Act now to resolve this matter and avoid additional consequences.

Yours faithfully,

Ahadi Collections Team
Debt Recovery Services
P.O. Box 12345, Nairobi
Email: collections@ahadi.co.ke
Phone: +254-700-123456

---
NOTICE: This is an attempt to collect a debt. Any information obtained will be used for that purpose. This communication is from a debt collector."""

        template = DemandLetterTemplate(
            id=str(uuid.uuid4()),
            name='First Notice - Payment Demand',
            subject='URGENT: Payment Demand - Account {ACCOUNT_NUMBER}',
            content=template_content,
            created_by=gm.id,
            active=True
        )
        
        db.session.add(template)
        db.session.commit()
        
        print("✅ Sample demand letter template created successfully!")
        print(f"Template ID: {template.id}")
        print(f"Template Name: {template.name}")
        print("\nTemplate uses these placeholders:")
        print("• {CLIENT_NAME} - Consumer's full name")
        print("• {ACCOUNT_NUMBER} - Account reference number")
        print("• {AMOUNT_DUE} - Outstanding balance")
        print("• {DATE} - Current date")
        
        # Create a second template for final notice
        final_notice_content = """FINAL NOTICE - LEGAL ACTION PENDING

Dear {CLIENT_NAME},

RE: FINAL DEMAND FOR PAYMENT - ACCOUNT NUMBER {ACCOUNT_NUMBER}

This is your FINAL NOTICE regarding the outstanding debt of {AMOUNT_DUE} on your account as of {DATE}.

Our previous correspondence dated earlier has been ignored, and no payment or contact has been received from you.

FINAL DEMAND:
You are hereby given FINAL NOTICE to pay the outstanding amount of {AMOUNT_DUE} within FORTY-EIGHT (48) HOURS of receiving this letter.

FAILURE TO PAY WILL RESULT IN:
• Immediate commencement of legal proceedings against you
• Additional legal costs and court fees being added to your debt
• Possible attachment of your assets and garnishment of wages
• Adverse credit bureau reporting affecting your credit score
• Public record of judgment against you

LEGAL ACTION IMMINENT:
Please be advised that we have instructed our legal department to prepare court documents. Legal proceedings will commence without further notice if payment is not received within the specified timeframe.

LAST OPPORTUNITY:
This is your final opportunity to resolve this matter before legal action. Contact us immediately at +254-700-123456 or visit our offices.

Do not ignore this notice. The consequences of non-payment are serious and will affect your financial standing.

URGENT ACTION REQUIRED - PAY NOW OR FACE LEGAL CONSEQUENCES

Yours faithfully,

Legal Collections Department
Ahadi Collections
P.O. Box 12345, Nairobi
Email: legal@ahadi.co.ke
Phone: +254-700-123456

---
FINAL LEGAL NOTICE: This is a final attempt to collect a debt before legal action. Immediate payment is required to avoid court proceedings."""

        final_template = DemandLetterTemplate(
            id=str(uuid.uuid4()),
            name='Final Notice - Legal Action Pending',
            subject='FINAL NOTICE: Legal Action Pending - Account {ACCOUNT_NUMBER}',
            content=final_notice_content,
            created_by=gm.id,
            active=True
        )
        
        db.session.add(final_template)
        db.session.commit()
        
        print(f"\n✅ Final notice template also created!")
        print(f"Template ID: {final_template.id}")
        print(f"Template Name: {final_template.name}")
        
        print(f"\n🎯 Total templates created: 2")
        print("You can now test the demand letter system!")

if __name__ == '__main__':
    create_sample_demand_letter_template()