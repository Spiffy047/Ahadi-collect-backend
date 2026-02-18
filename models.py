from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
import json
import uuid

db = SQLAlchemy()

# User Management
class User(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('administrator', 'general_manager', 'collections_manager', 'collections_officer'), nullable=False)
    region_id = db.Column(db.String(50), db.ForeignKey('region.id'))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    region = db.relationship('Region', backref='users')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Region(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(10), unique=True, nullable=False)
    counties = db.Column(db.Text)  # JSON array of counties
    active = db.Column(db.Boolean, default=True)

# Core Entities
class Consumer(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    national_id = db.Column(db.String(20))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address_street = db.Column(db.String(200))
    address_city = db.Column(db.String(100))
    address_county = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    location_verified = db.Column(db.Boolean, default=False)
    location_verified_by = db.Column(db.String(50), db.ForeignKey('user.id'))
    location_verified_at = db.Column(db.DateTime)
    region_id = db.Column(db.String(50), db.ForeignKey('region.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    region = db.relationship('Region')
    accounts = db.relationship('Account', backref='consumer')
    location_verifier = db.relationship('User', foreign_keys=[location_verified_by])

class Account(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    consumer_id = db.Column(db.String(50), db.ForeignKey('consumer.id'), nullable=False)
    creditor_id = db.Column(db.String(50), db.ForeignKey('creditor.id'), nullable=False)
    account_number = db.Column(db.String(100), nullable=False)
    original_balance = db.Column(db.Numeric(15, 2), nullable=False)
    current_balance = db.Column(db.Numeric(15, 2), nullable=False)
    principal_balance = db.Column(db.Numeric(15, 2), default=0)
    interest_balance = db.Column(db.Numeric(15, 2), default=0)
    fee_balance = db.Column(db.Numeric(15, 2), default=0)
    status = db.Column(db.Enum('active', 'paid_in_full', 'settled', 'closed', 'forwarded'), default='active')
    placement_date = db.Column(db.Date)
    assigned_officer_id = db.Column(db.String(50), db.ForeignKey('user.id'))
    collateral_type = db.Column(db.Enum('land', 'motor_vehicle', 'chattels', 'unsecured', 'guarantor', 'salary', name='collateral_type'), default='unsecured')
    collateral_status = db.Column(db.Enum('available', 'repossessed', 'sold', 'under_valuation', 'disputed', 'not_applicable', name='collateral_status'), default='not_applicable')
    collateral_value = db.Column(db.Numeric(15, 2))
    collateral_description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    creditor = db.relationship('Creditor')
    assigned_officer = db.relationship('User')
    payments = db.relationship('Payment', backref='account')

class Creditor(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    short_name = db.Column(db.String(50), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    contact_email = db.Column(db.String(100))
    contact_phone = db.Column(db.String(20))
    commission_rate = db.Column(db.Numeric(5, 2))
    active = db.Column(db.Boolean, default=True)

class Payment(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    account_id = db.Column(db.String(50), db.ForeignKey('account.id'), nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    payment_method = db.Column(db.Enum('mpesa', 'bank_transfer', 'cash', 'cheque'), nullable=False)
    status = db.Column(db.Enum('pending', 'completed', 'failed'), default='pending')
    processed_date = db.Column(db.DateTime)
    reference_number = db.Column(db.String(100))
    created_by = db.Column(db.String(50), db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    created_by_user = db.relationship('User')

class PromiseToPay(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    account_id = db.Column(db.String(50), db.ForeignKey('account.id'), nullable=False)
    consumer_id = db.Column(db.String(50), db.ForeignKey('consumer.id'), nullable=False)
    promised_amount = db.Column(db.Numeric(15, 2), nullable=False)
    promised_date = db.Column(db.Date, nullable=False)
    payment_method = db.Column(db.Enum('mpesa', 'bank_transfer', 'cash', 'cheque', 'salary_deduction', 'asset_sale', 'family_support', 'business_income', 'loan_refinance', 'partial_settlement'), nullable=False)
    contact_method = db.Column(db.Enum('phone_call', 'sms', 'email', 'whatsapp', 'field_visit', 'office_visit', 'letter'), default='phone_call')
    consumer_response = db.Column(db.Enum('PTP', 'LMES', 'RECAL', 'NCOM', 'SPTP', 'UNC', 'cooperative', 'hostile', 'evasive', 'unavailable', 'disputed_debt', 'financial_hardship', 'willing_to_pay'), default='cooperative')
    follow_up_action = db.Column(db.Enum('call_back', 'field_visit', 'send_letter', 'escalate', 'legal_action', 'settlement_offer', 'payment_plan'), default='call_back')
    status = db.Column(db.Enum('active', 'kept', 'broken', 'cancelled'), default='active')
    notes = db.Column(db.Text)
    created_by = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    kept_date = db.Column(db.DateTime)
    broken_date = db.Column(db.DateTime)
    
    account = db.relationship('Account')
    consumer = db.relationship('Consumer')
    created_by_user = db.relationship('User')
    ptp_notes = db.relationship('PTPNote', backref='promise_to_pay', order_by='PTPNote.created_at')

class PTPNote(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    ptp_id = db.Column(db.String(50), db.ForeignKey('promise_to_pay.id'), nullable=False)
    note = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    created_by_user = db.relationship('User')

class Escalation(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    account_id = db.Column(db.String(50), db.ForeignKey('account.id'), nullable=False)
    escalated_by = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)
    escalated_to = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('pending', 'acknowledged', 'resolved'), default='pending')
    priority = db.Column(db.Enum('low', 'medium', 'high', 'urgent'), default='medium')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    acknowledged_at = db.Column(db.DateTime)
    resolved_at = db.Column(db.DateTime)
    resolution_notes = db.Column(db.Text)
    
    account = db.relationship('Account')
    escalated_by_user = db.relationship('User', foreign_keys=[escalated_by])
    escalated_to_user = db.relationship('User', foreign_keys=[escalated_to])

# Additional Tables for Comprehensive Testing
class PaymentSchedule(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    account_id = db.Column(db.String(50), db.ForeignKey('account.id'), nullable=False)
    total_amount = db.Column(db.Numeric(15, 2), nullable=False)
    payment_amount = db.Column(db.Numeric(15, 2), nullable=False)
    frequency = db.Column(db.Enum('weekly', 'monthly', 'quarterly'), default='monthly')
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    status = db.Column(db.Enum('active', 'completed', 'cancelled'), default='active')
    created_by = db.Column(db.String(50), db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    account = db.relationship('Account')
    created_by_user = db.relationship('User')

class Settlement(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    account_id = db.Column(db.String(50), db.ForeignKey('account.id'), nullable=False)
    original_balance = db.Column(db.Numeric(15, 2), nullable=False)
    settlement_amount = db.Column(db.Numeric(15, 2), nullable=False)
    discount_percentage = db.Column(db.Numeric(5, 2))
    status = db.Column(db.Enum('proposed', 'approved', 'rejected', 'completed'), default='proposed')
    proposed_date = db.Column(db.DateTime, default=datetime.utcnow)
    approved_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    created_by = db.Column(db.String(50), db.ForeignKey('user.id'))
    
    account = db.relationship('Account')
    created_by_user = db.relationship('User')

class AREvent(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    account_id = db.Column(db.String(50), db.ForeignKey('account.id'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.String(50), db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    account = db.relationship('Account')
    created_by_user = db.relationship('User')

class BatchJob(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    job_type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.Enum('pending', 'processing', 'completed', 'failed'), default='pending')
    total_records = db.Column(db.Integer, default=0)
    processed_records = db.Column(db.Integer, default=0)
    success_records = db.Column(db.Integer, default=0)
    failed_records = db.Column(db.Integer, default=0)
    created_by = db.Column(db.String(50), db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    created_by_user = db.relationship('User')

# Tagging System
class Tag(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.Enum('consumer', 'account', 'creditor', 'office', 'workgroup', 'image'), nullable=False)
    color = db.Column(db.String(7))
    active = db.Column(db.Boolean, default=True)

class EntityTag(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    tag_id = db.Column(db.String(50), db.ForeignKey('tag.id'), nullable=False)
    entity_type = db.Column(db.String(50), nullable=False)
    entity_id = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    tag = db.relationship('Tag')

# Job System
class Job(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    job_type = db.Column(db.Enum('email_alert', 'report_generation', 'data_cleanup', 'backup'), nullable=False)
    schedule = db.Column(db.String(100))  # Cron expression
    status = db.Column(db.Enum('idle', 'running', 'completed', 'failed'), default='idle')
    last_run = db.Column(db.DateTime)
    next_run = db.Column(db.DateTime)
    enabled = db.Column(db.Boolean, default=True)
    config = db.Column(db.Text)  # JSON config

class JobExecution(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    job_id = db.Column(db.String(50), db.ForeignKey('job.id'), nullable=False)
    status = db.Column(db.Enum('running', 'completed', 'failed'), nullable=False)
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    result = db.Column(db.Text)
    emails_sent = db.Column(db.Integer, default=0)
    
    job = db.relationship('Job')

# Alert System
class Alert(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    alert_type = db.Column(db.Enum('payment_due', 'payment_overdue', 'ptp_due', 'ptp_broken', 'high_priority'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    priority = db.Column(db.Enum('low', 'medium', 'high', 'critical'), default='medium')
    account_id = db.Column(db.String(50), db.ForeignKey('account.id'))
    consumer_id = db.Column(db.String(50), db.ForeignKey('consumer.id'))
    assigned_to = db.Column(db.String(50), db.ForeignKey('user.id'))
    status = db.Column(db.Enum('active', 'acknowledged', 'resolved'), default='active')
    due_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    acknowledged_at = db.Column(db.DateTime)
    resolved_at = db.Column(db.DateTime)
    
    account = db.relationship('Account')
    consumer = db.relationship('Consumer')
    assigned_user = db.relationship('User')

class EmailNotification(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    recipient_email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    alert_id = db.Column(db.String(50), db.ForeignKey('alert.id'))
    report_execution_id = db.Column(db.String(50), db.ForeignKey('report_execution.id'))
    status = db.Column(db.Enum('pending', 'sent', 'failed'), default='pending')
    sent_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    alert = db.relationship('Alert')
    report_execution = db.relationship('ReportExecution')
class UDDTable(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    table_name = db.Column(db.String(100), unique=True, nullable=False)
    fields = db.Column(db.Text, nullable=False)  # JSON field definitions
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class UDDRecord(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    table_name = db.Column(db.String(100), nullable=False)
    data = db.Column(db.Text, nullable=False)  # JSON data
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Automated Report System
class ReportTemplate(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    report_type = db.Column(db.Enum('daily', 'weekly', 'monthly'), nullable=False)
    recipients = db.Column(db.Text, nullable=False)  # JSON array of user IDs
    template_config = db.Column(db.Text, nullable=False)  # JSON config
    active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.String(50), db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    created_by_user = db.relationship('User')

class ReportExecution(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    template_id = db.Column(db.String(50), db.ForeignKey('report_template.id'), nullable=False)
    report_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum('generating', 'completed', 'failed'), default='generating')
    report_data = db.Column(db.Text)  # JSON report data
    email_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    template = db.relationship('ReportTemplate')

# Demand Letter System
class DemandLetterTemplate(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text, nullable=False)  # Template with placeholders
    active = db.Column(db.Boolean, default=True)
    created_by = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    created_by_user = db.relationship('User')

# Advanced Analytics Models
class RiskScore(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    consumer_id = db.Column(db.String(50), db.ForeignKey('consumer.id'), nullable=False)
    account_id = db.Column(db.String(50), db.ForeignKey('account.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)  # 0-1000 scale
    risk_level = db.Column(db.Enum('low', 'medium', 'high', 'critical', 'default'), nullable=False)
    factors = db.Column(db.Text)  # JSON of risk factors
    calculated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    consumer = db.relationship('Consumer')
    account = db.relationship('Account')

class RecoveryForecast(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    forecast_date = db.Column(db.Date, nullable=False)
    predicted_amount = db.Column(db.Numeric(15, 2), nullable=False)
    actual_amount = db.Column(db.Numeric(15, 2))
    confidence_level = db.Column(db.Numeric(5, 2))  # Percentage
    region_id = db.Column(db.String(50), db.ForeignKey('region.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    region = db.relationship('Region')

class PortfolioMetrics(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    metric_date = db.Column(db.Date, nullable=False)
    par_1_30_accounts = db.Column(db.Integer, default=0)
    par_1_30_amount = db.Column(db.Numeric(15, 2), default=0)
    par_31_60_accounts = db.Column(db.Integer, default=0)
    par_31_60_amount = db.Column(db.Numeric(15, 2), default=0)
    par_61_90_accounts = db.Column(db.Integer, default=0)
    par_61_90_amount = db.Column(db.Numeric(15, 2), default=0)
    par_90_plus_accounts = db.Column(db.Integer, default=0)
    par_90_plus_amount = db.Column(db.Numeric(15, 2), default=0)
    collection_rate = db.Column(db.Numeric(5, 2))
    recovery_rate = db.Column(db.Numeric(5, 2))
    cure_rate = db.Column(db.Numeric(5, 2))
    ptp_fulfillment_rate = db.Column(db.Numeric(5, 2))
    region_id = db.Column(db.String(50), db.ForeignKey('region.id'))
    
    region = db.relationship('Region')

class LegalCase(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    account_id = db.Column(db.String(50), db.ForeignKey('account.id'), nullable=False)
    case_number = db.Column(db.String(100))
    case_type = db.Column(db.Enum('demand_letter', 'court_case', 'arbitration', 'repossession'), nullable=False)
    status = db.Column(db.Enum('pending', 'in_progress', 'settled', 'dismissed', 'won', 'lost'), default='pending')
    filed_date = db.Column(db.Date)
    resolution_date = db.Column(db.Date)
    recovery_amount = db.Column(db.Numeric(15, 2))
    legal_costs = db.Column(db.Numeric(15, 2))
    assigned_firm = db.Column(db.String(200))
    notes = db.Column(db.Text)
    created_by = db.Column(db.String(50), db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    account = db.relationship('Account')
    created_by_user = db.relationship('User')

class EarlyWarningSignal(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    account_id = db.Column(db.String(50), db.ForeignKey('account.id'), nullable=False)
    signal_type = db.Column(db.Enum('payment_delay', 'contact_failure', 'broken_ptp', 'balance_increase'), nullable=False)
    severity = db.Column(db.Enum('low', 'medium', 'high', 'critical'), default='medium')
    description = db.Column(db.Text, nullable=False)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    status = db.Column(db.Enum('active', 'resolved', 'ignored'), default='active')
    
    account = db.relationship('Account')

class ServiceProvider(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    service_type = db.Column(db.Enum('vehicle_repossession', 'property_valuation', 'legal_services', 'debt_collection', 'asset_recovery'), nullable=False)
    contact_person = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    coverage_areas = db.Column(db.Text)  # JSON array of counties/regions
    rating = db.Column(db.Numeric(3, 2))  # 1.00 to 5.00
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
class CollateralAsset(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    account_id = db.Column(db.String(50), db.ForeignKey('account.id'), nullable=False)
    asset_type = db.Column(db.Enum('land', 'motor_vehicle', 'machinery', 'property', 'other'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    estimated_value = db.Column(db.Numeric(15, 2))
    current_status = db.Column(db.Enum('available', 'repossessed', 'sold', 'under_valuation', 'disputed', 'repossess', 'successful', 'no_bid', 'low_bid', 'shortfall', 'claim_with_insurance', 'insurance_claimed', 'ipf_cancelled', 'demand_running', 'injunction', '40_sn', '45_days', '90_sn', 'mv_sale_approved'), default='available')
    location_address = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    assigned_provider_id = db.Column(db.String(50), db.ForeignKey('service_provider.id'))
    registration_number = db.Column(db.String(100))  # For vehicles/machinery
    title_deed_number = db.Column(db.String(100))  # For land/property
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    account = db.relationship('Account')
    assigned_provider = db.relationship('ServiceProvider')

class ExternalReceiver(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    receiver_type = db.Column(db.Enum('law_firm', 'debt_collector', 'recovery_agent', 'auction_house', 'liquidator'), nullable=False)
    contact_person = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    commission_rate = db.Column(db.Numeric(5, 2))  # Percentage
    success_rate = db.Column(db.Numeric(5, 2))  # Percentage
    coverage_areas = db.Column(db.Text)  # JSON array
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AccountForwarding(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    account_id = db.Column(db.String(50), db.ForeignKey('account.id'), nullable=False)
    receiver_id = db.Column(db.String(50), db.ForeignKey('external_receiver.id'), nullable=False)
    forwarded_date = db.Column(db.Date, nullable=False)
    forwarded_balance = db.Column(db.Numeric(15, 2), nullable=False)
    status = db.Column(db.Enum('forwarded', 'in_progress', 'recalled', 'settled', 'written_off'), default='forwarded')
    recall_date = db.Column(db.Date)
    recall_reason = db.Column(db.Text)
    recovery_amount = db.Column(db.Numeric(15, 2))
    commission_paid = db.Column(db.Numeric(15, 2))
    notes = db.Column(db.Text)
    created_by = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    account = db.relationship('Account')
    receiver = db.relationship('ExternalReceiver')
    created_by_user = db.relationship('User')
class DemandLetter(db.Model):
    id = db.Column(db.String(50), primary_key=True)
    template_id = db.Column(db.String(50), db.ForeignKey('demand_letter_template.id'), nullable=False)
    account_id = db.Column(db.String(50), db.ForeignKey('account.id'), nullable=False)
    consumer_id = db.Column(db.String(50), db.ForeignKey('consumer.id'), nullable=False)
    generated_content = db.Column(db.Text, nullable=False)
    status = db.Column(db.Enum('draft', 'sent', 'delivered'), default='draft')
    created_by = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    template = db.relationship('DemandLetterTemplate')
    account = db.relationship('Account')
    consumer = db.relationship('Consumer')
    created_by_user = db.relationship('User')