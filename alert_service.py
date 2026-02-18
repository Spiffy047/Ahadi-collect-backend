import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import uuid
from models import db, Alert, EmailNotification, Account, Consumer, User, PromiseToPay
from sqlalchemy import and_, or_

class EmailService:
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587, username="", password=""):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
    
    def send_email(self, to_email, subject, body):
        """Send email notification"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            # For demo purposes, we'll just log the email instead of actually sending
            print(f"EMAIL SENT TO: {to_email}")
            print(f"SUBJECT: {subject}")
            print(f"BODY: {body[:200]}...")
            return True
            
            # Uncomment below for actual email sending
            # server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            # server.starttls()
            # server.login(self.username, self.password)
            # text = msg.as_string()
            # server.sendmail(self.username, to_email, text)
            # server.quit()
            # return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

class AlertService:
    def __init__(self, email_service=None):
        self.email_service = email_service or EmailService()
    
    def create_alert(self, alert_type, title, message, priority='medium', account_id=None, 
                    consumer_id=None, assigned_to=None, due_date=None):
        """Create a new alert"""
        alert = Alert(
            id=str(uuid.uuid4()),
            alert_type=alert_type,
            title=title,
            message=message,
            priority=priority,
            account_id=account_id,
            consumer_id=consumer_id,
            assigned_to=assigned_to,
            due_date=due_date
        )
        db.session.add(alert)
        db.session.commit()
        return alert
    
    def send_notification_email(self, alert, recipient_email):
        """Send email notification for alert"""
        subject = f"[{alert.priority.upper()}] {alert.title}"
        
        body = f"""
        <html>
        <body>
            <h2>Collections Alert Notification</h2>
            <p><strong>Alert Type:</strong> {alert.alert_type.replace('_', ' ').title()}</p>
            <p><strong>Priority:</strong> {alert.priority.upper()}</p>
            <p><strong>Message:</strong> {alert.message}</p>
            {f'<p><strong>Due Date:</strong> {alert.due_date.strftime("%Y-%m-%d")}</p>' if alert.due_date else ''}
            {f'<p><strong>Account ID:</strong> {alert.account_id}</p>' if alert.account_id else ''}
            {f'<p><strong>Consumer:</strong> {alert.consumer.first_name} {alert.consumer.last_name}</p>' if alert.consumer else ''}
            <p><strong>Created:</strong> {alert.created_at.strftime("%Y-%m-%d %H:%M")}</p>
            <hr>
            <p><small>DM9 Collections Management System</small></p>
        </body>
        </html>
        """
        
        # Create email notification record
        notification = EmailNotification(
            id=str(uuid.uuid4()),
            recipient_email=recipient_email,
            subject=subject,
            body=body,
            alert_id=alert.id
        )
        db.session.add(notification)
        
        # Send email
        if self.email_service.send_email(recipient_email, subject, body):
            notification.status = 'sent'
            notification.sent_at = datetime.utcnow()
        else:
            notification.status = 'failed'
        
        db.session.commit()
        return notification
    
    def check_payment_due_alerts(self):
        """Check for payments due in 5 days and create alerts"""
        five_days_from_now = datetime.utcnow().date() + timedelta(days=5)
        
        # Check Promise to Pay due dates
        ptps_due = PromiseToPay.query.filter(
            and_(
                PromiseToPay.promised_date == five_days_from_now,
                PromiseToPay.status == 'active'
            )
        ).all()
        
        for ptp in ptps_due:
            # Check if alert already exists
            existing_alert = Alert.query.filter(
                and_(
                    Alert.alert_type == 'payment_due',
                    Alert.account_id == ptp.account_id,
                    Alert.due_date == ptp.promised_date,
                    Alert.status == 'active'
                )
            ).first()
            
            if not existing_alert:
                alert = self.create_alert(
                    alert_type='payment_due',
                    title=f'Payment Due in 5 Days - {ptp.account.account_number}',
                    message=f'Customer {ptp.consumer.first_name} {ptp.consumer.last_name} has a payment of KES {ptp.promised_amount:,.2f} due on {ptp.promised_date.strftime("%Y-%m-%d")}',
                    priority='high',
                    account_id=ptp.account_id,
                    consumer_id=ptp.consumer_id,
                    assigned_to=ptp.account.assigned_officer_id,
                    due_date=ptp.promised_date
                )
                
                # Send notifications to assigned officer and manager
                self._send_alert_notifications(alert)
    
    def check_overdue_payments(self):
        """Check for overdue payments and create alerts"""
        today = datetime.utcnow().date()
        
        # Check overdue Promise to Pay
        overdue_ptps = PromiseToPay.query.filter(
            and_(
                PromiseToPay.promised_date < today,
                PromiseToPay.status == 'active'
            )
        ).all()
        
        for ptp in overdue_ptps:
            days_overdue = (today - ptp.promised_date).days
            
            # Check if alert already exists for this overdue payment
            existing_alert = Alert.query.filter(
                and_(
                    Alert.alert_type == 'payment_overdue',
                    Alert.account_id == ptp.account_id,
                    Alert.due_date == ptp.promised_date,
                    Alert.status == 'active'
                )
            ).first()
            
            if not existing_alert:
                priority = 'critical' if days_overdue > 7 else 'high'
                
                alert = self.create_alert(
                    alert_type='payment_overdue',
                    title=f'Payment Overdue - {ptp.account.account_number}',
                    message=f'Customer {ptp.consumer.first_name} {ptp.consumer.last_name} payment of KES {ptp.promised_amount:,.2f} is {days_overdue} days overdue (due: {ptp.promised_date.strftime("%Y-%m-%d")})',
                    priority=priority,
                    account_id=ptp.account_id,
                    consumer_id=ptp.consumer_id,
                    assigned_to=ptp.account.assigned_officer_id,
                    due_date=ptp.promised_date
                )
                
                # Mark PTP as broken
                ptp.status = 'broken'
                ptp.broken_date = datetime.utcnow()
                
                # Send notifications
                self._send_alert_notifications(alert)
        
        db.session.commit()
    
    def check_high_priority_accounts(self):
        """Check for high priority accounts (high balance, long overdue) and auto-escalate after 30 days"""
        from models import Escalation, AREvent
        
        # Accounts with balance > 200,000 KES (Critical Risk) or > 100,000 KES (High Risk)
        thirty_days_ago = datetime.utcnow().date() - timedelta(days=30)
        ninety_days_ago = datetime.utcnow().date() - timedelta(days=90)
        
        # Critical accounts (>200K, >30 days)
        critical_accounts = Account.query.filter(
            and_(
                Account.current_balance > 200000,
                Account.placement_date < thirty_days_ago,
                Account.status == 'active'
            )
        ).all()
        
        for account in critical_accounts:
            days_since_placement = (datetime.utcnow().date() - account.placement_date).days
            
            # Auto-escalate every 30 days
            if days_since_placement % 30 == 0:
                # Check if escalation already exists for this period
                existing_escalation = Escalation.query.filter(
                    and_(
                        Escalation.account_id == account.id,
                        Escalation.status.in_(['pending', 'acknowledged']),
                        Escalation.created_at >= datetime.utcnow() - timedelta(days=5)
                    )
                ).first()
                
                if not existing_escalation and account.assigned_officer_id:
                    officer = User.query.get(account.assigned_officer_id)
                    if officer and officer.region_id:
                        manager = User.query.filter(
                            and_(
                                User.role == 'collections_manager',
                                User.region_id == officer.region_id,
                                User.active == True
                            )
                        ).first()
                        
                        if manager:
                            escalation = Escalation(
                                id=str(uuid.uuid4()),
                                account_id=account.id,
                                escalated_by=account.assigned_officer_id,
                                escalated_to=manager.id,
                                reason=f'Auto-escalation: Critical account (KES {account.current_balance:,.2f}) overdue for {days_since_placement} days',
                                priority='critical'
                            )
                            db.session.add(escalation)
                            
                            ar_event = AREvent(
                                id=str(uuid.uuid4()),
                                account_id=account.id,
                                event_type='escalation',
                                description=f'Auto-escalated to manager after {days_since_placement} days',
                                created_by=account.assigned_officer_id
                            )
                            db.session.add(ar_event)
            
            # Create alert
            existing_alert = Alert.query.filter(
                and_(
                    Alert.alert_type == 'high_priority',
                    Alert.account_id == account.id,
                    Alert.status == 'active'
                )
            ).first()
            
            if not existing_alert:
                alert = self.create_alert(
                    alert_type='high_priority',
                    title=f'Critical Account - {account.account_number}',
                    message=f'Account with balance KES {account.current_balance:,.2f} has been active for {days_since_placement} days without resolution',
                    priority='critical',
                    account_id=account.id,
                    consumer_id=account.consumer_id,
                    assigned_to=account.assigned_officer_id
                )
                self._send_alert_notifications(alert)
        
        # High priority accounts (>100K, >90 days)
        high_priority_accounts = Account.query.filter(
            and_(
                Account.current_balance > 100000,
                Account.current_balance <= 200000,
                Account.placement_date < ninety_days_ago,
                Account.status == 'active'
            )
        ).all()
        
        for account in high_priority_accounts:
            days_since_placement = (datetime.utcnow().date() - account.placement_date).days
            
            # Auto-escalate every 30 days
            if days_since_placement % 30 == 0:
                existing_escalation = Escalation.query.filter(
                    and_(
                        Escalation.account_id == account.id,
                        Escalation.status.in_(['pending', 'acknowledged']),
                        Escalation.created_at >= datetime.utcnow() - timedelta(days=5)
                    )
                ).first()
                
                if not existing_escalation and account.assigned_officer_id:
                    officer = User.query.get(account.assigned_officer_id)
                    if officer and officer.region_id:
                        manager = User.query.filter(
                            and_(
                                User.role == 'collections_manager',
                                User.region_id == officer.region_id,
                                User.active == True
                            )
                        ).first()
                        
                        if manager:
                            escalation = Escalation(
                                id=str(uuid.uuid4()),
                                account_id=account.id,
                                escalated_by=account.assigned_officer_id,
                                escalated_to=manager.id,
                                reason=f'Auto-escalation: High-risk account (KES {account.current_balance:,.2f}) overdue for {days_since_placement} days',
                                priority='high'
                            )
                            db.session.add(escalation)
                            
                            ar_event = AREvent(
                                id=str(uuid.uuid4()),
                                account_id=account.id,
                                event_type='escalation',
                                description=f'Auto-escalated to manager after {days_since_placement} days',
                                created_by=account.assigned_officer_id
                            )
                            db.session.add(ar_event)
            
            existing_alert = Alert.query.filter(
                and_(
                    Alert.alert_type == 'high_priority',
                    Alert.account_id == account.id,
                    Alert.status == 'active'
                )
            ).first()
            
            if not existing_alert:
                alert = self.create_alert(
                    alert_type='high_priority',
                    title=f'High Priority Account - {account.account_number}',
                    message=f'Account with balance KES {account.current_balance:,.2f} has been active for {days_since_placement} days without resolution',
                    priority='high',
                    account_id=account.id,
                    consumer_id=account.consumer_id,
                    assigned_to=account.assigned_officer_id
                )
                self._send_alert_notifications(alert)
        
        db.session.commit()
    
    def _send_alert_notifications(self, alert):
        """Send alert notifications to relevant users"""
        recipients = []
        
        # Add assigned officer
        if alert.assigned_to:
            officer = User.query.get(alert.assigned_to)
            if officer and officer.email:
                recipients.append(officer.email)
        
        # Add managers in the same region
        if alert.assigned_user and alert.assigned_user.region_id:
            managers = User.query.filter(
                and_(
                    User.role == 'collections_manager',
                    User.region_id == alert.assigned_user.region_id,
                    User.active == True
                )
            ).all()
            
            for manager in managers:
                if manager.email:
                    recipients.append(manager.email)
        
        # Add administrators for critical alerts
        if alert.priority == 'critical':
            admins = User.query.filter(
                and_(
                    User.role == 'administrator',
                    User.active == True
                )
            ).all()
            
            for admin in admins:
                if admin.email:
                    recipients.append(admin.email)
        
        # Send notifications
        for email in set(recipients):  # Remove duplicates
            self.send_notification_email(alert, email)
    
    def run_daily_checks(self):
        """Run all daily alert checks"""
        print("Running daily alert checks...")
        self.check_payment_due_alerts()
        self.check_overdue_payments()
        self.check_high_priority_accounts()
        print("Daily alert checks completed")

# Initialize alert service
alert_service = AlertService()