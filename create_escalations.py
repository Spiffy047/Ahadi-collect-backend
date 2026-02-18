from app import app
from models import *
from datetime import datetime, timedelta
import uuid

with app.app_context():
    # Get some accounts and users for escalations
    accounts = Account.query.limit(5).all()
    officers = User.query.filter_by(role='collections_officer').all()
    managers = User.query.filter_by(role='collections_manager').all()

    if accounts and officers and managers:
        escalations_data = [
            {
                'account': accounts[0],
                'officer': officers[0],
                'manager': managers[0],
                'reason': 'Consumer unreachable for 30+ days',
                'priority': 'high',
                'status': 'pending',
                'days_ago': 2
            },
            {
                'account': accounts[1],
                'officer': officers[1] if len(officers) > 1 else officers[0],
                'manager': managers[0],
                'reason': 'Disputed debt amount - requires manager review',
                'priority': 'medium',
                'status': 'acknowledged',
                'days_ago': 5
            },
            {
                'account': accounts[2],
                'officer': officers[0],
                'manager': managers[0],
                'reason': 'Consumer requesting payment plan modification',
                'priority': 'medium',
                'status': 'resolved',
                'days_ago': 10
            },
            {
                'account': accounts[3],
                'officer': officers[1] if len(officers) > 1 else officers[0],
                'manager': managers[0],
                'reason': 'High-value account with no response to multiple contacts',
                'priority': 'critical',
                'status': 'pending',
                'days_ago': 1
            },
            {
                'account': accounts[4],
                'officer': officers[0],
                'manager': managers[0],
                'reason': 'Consumer claims account paid in full - verification needed',
                'priority': 'high',
                'status': 'acknowledged',
                'days_ago': 3
            }
        ]
        
        for esc_data in escalations_data:
            created_date = datetime.utcnow() - timedelta(days=esc_data['days_ago'])
            
            escalation = Escalation(
                id=str(uuid.uuid4()),
                account_id=esc_data['account'].id,
                escalated_by=esc_data['officer'].id,
                escalated_to=esc_data['manager'].id,
                reason=esc_data['reason'],
                priority=esc_data['priority'],
                status=esc_data['status'],
                created_at=created_date
            )
            
            if esc_data['status'] == 'acknowledged':
                escalation.acknowledged_at = created_date + timedelta(hours=2)
            elif esc_data['status'] == 'resolved':
                escalation.acknowledged_at = created_date + timedelta(hours=1)
                escalation.resolved_at = created_date + timedelta(days=2)
                escalation.resolution_notes = 'Issue resolved through direct manager intervention'
            
            db.session.add(escalation)
        
        db.session.commit()
        print(f'Created {len(escalations_data)} escalation cases')
    else:
        print('No accounts, officers, or managers found to create escalations')