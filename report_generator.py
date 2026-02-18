import json
import uuid
from datetime import datetime, date, timedelta
from sqlalchemy import func, and_
from models import (
    db, User, Account, Payment, PromiseToPay, Consumer, Region,
    ReportTemplate, ReportExecution
)
from email_service import email_service

class ReportGenerator:
    
    def generate_daily_report(self, region_id=None, user_id=None):
        """Generate daily performance report"""
        today = date.today()
        
        # Base query filters
        filters = []
        if region_id:
            filters.append(User.region_id == region_id)
        if user_id:
            filters.append(User.id == user_id)
        
        # Get accounts data
        accounts_query = db.session.query(Account).join(User, Account.assigned_officer_id == User.id)
        if filters:
            accounts_query = accounts_query.filter(and_(*filters))
        
        total_accounts = accounts_query.count()
        total_balance = accounts_query.with_entities(func.sum(Account.current_balance)).scalar() or 0
        
        # Get today's payments
        payments_today = db.session.query(Payment).filter(
            func.date(Payment.processed_date) == today,
            Payment.status == 'completed'
        )
        if region_id:
            payments_today = payments_today.join(Account).join(User, Account.assigned_officer_id == User.id).filter(User.region_id == region_id)
        
        collections_today = payments_today.count()
        amount_collected_today = payments_today.with_entities(func.sum(Payment.amount)).scalar() or 0
        
        # Get officer performance
        officer_performance = []
        officers_query = db.session.query(User).filter(User.role == 'collections_officer')
        if filters:
            officers_query = officers_query.filter(and_(*filters))
        
        for officer in officers_query.all():
            officer_accounts = Account.query.filter_by(assigned_officer_id=officer.id).count()
            officer_payments = Payment.query.join(Account).filter(
                Account.assigned_officer_id == officer.id,
                func.date(Payment.processed_date) == today,
                Payment.status == 'completed'
            )
            officer_collections = officer_payments.count()
            officer_amount = officer_payments.with_entities(func.sum(Payment.amount)).scalar() or 0
            officer_ptps = PromiseToPay.query.join(Account).filter(
                Account.assigned_officer_id == officer.id,
                func.date(PromiseToPay.created_at) == today
            ).count()
            
            officer_performance.append({
                'name': f"{officer.username}",
                'accounts': officer_accounts,
                'collections': officer_collections,
                'amount': float(officer_amount),
                'ptps': officer_ptps
            })
        
        return {
            'total_accounts': total_accounts,
            'total_balance': float(total_balance),
            'collections_today': collections_today,
            'amount_collected_today': float(amount_collected_today),
            'officer_performance': officer_performance,
            'report_date': today.isoformat()
        }
    
    def generate_weekly_report(self, region_id=None, user_id=None):
        """Generate weekly performance report"""
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
        
        # Similar to daily but for week range
        filters = []
        if region_id:
            filters.append(User.region_id == region_id)
        if user_id:
            filters.append(User.id == user_id)
        
        # Get week's payments
        payments_week = db.session.query(Payment).filter(
            Payment.processed_date >= week_start,
            Payment.processed_date <= today,
            Payment.status == 'completed'
        )
        if region_id:
            payments_week = payments_week.join(Account).join(User, Account.assigned_officer_id == User.id).filter(User.region_id == region_id)
        
        collections_week = payments_week.count()
        amount_collected_week = payments_week.with_entities(func.sum(Payment.amount)).scalar() or 0
        
        return {
            'total_accounts': self.generate_daily_report(region_id, user_id)['total_accounts'],
            'total_balance': self.generate_daily_report(region_id, user_id)['total_balance'],
            'collections_week': collections_week,
            'amount_collected_week': float(amount_collected_week),
            'week_start': week_start.isoformat(),
            'week_end': today.isoformat()
        }
    
    def execute_scheduled_reports(self):
        """Execute all scheduled reports"""
        today = date.today()
        
        # Get all active report templates
        templates = ReportTemplate.query.filter_by(active=True).all()
        
        for template in templates:
            # Check if report already generated today
            existing = ReportExecution.query.filter_by(
                template_id=template.id,
                report_date=today
            ).first()
            
            if existing:
                continue
            
            # Generate report based on type
            config = json.loads(template.template_config)
            region_id = config.get('region_id')
            
            if template.report_type == 'daily':
                report_data = self.generate_daily_report(region_id)
            elif template.report_type == 'weekly' and today.weekday() == 0:  # Monday
                report_data = self.generate_weekly_report(region_id)
            else:
                continue
            
            # Create report execution record
            execution = ReportExecution(
                id=str(uuid.uuid4()),
                template_id=template.id,
                report_date=today,
                status='completed',
                report_data=json.dumps(report_data),
                completed_at=datetime.utcnow()
            )
            db.session.add(execution)
            db.session.commit()
            
            # Send emails
            email_service.send_report_email(execution.id)
            execution.email_sent = True
            db.session.commit()
    
    def create_report_template(self, name, report_type, recipients, config, created_by):
        """Create a new report template"""
        template = ReportTemplate(
            id=str(uuid.uuid4()),
            name=name,
            report_type=report_type,
            recipients=json.dumps(recipients),
            template_config=json.dumps(config),
            created_by=created_by
        )
        db.session.add(template)
        db.session.commit()
        return template

report_generator = ReportGenerator()