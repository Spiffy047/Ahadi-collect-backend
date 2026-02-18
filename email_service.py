import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, date
from models import db, EmailNotification, User, ReportExecution
import uuid

class EmailService:
    def __init__(self, smtp_server='smtp.gmail.com', smtp_port=587, username=None, password=None):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username or 'collections@company.com'
        self.password = password or 'app_password'
    
    def send_email(self, to_email, subject, body, is_html=True):
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.username
            msg['To'] = to_email
            msg['Subject'] = subject
            
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            # For demo purposes, we'll just log the email
            print(f"EMAIL SENT TO: {to_email}")
            print(f"SUBJECT: {subject}")
            print(f"BODY: {body[:200]}...")
            
            return True
        except Exception as e:
            print(f"Email send failed: {str(e)}")
            return False
    
    def send_report_email(self, report_execution_id):
        execution = ReportExecution.query.get(report_execution_id)
        if not execution or not execution.report_data:
            return False
        
        report_data = json.loads(execution.report_data)
        template = execution.template
        recipients = json.loads(template.recipients)
        
        # Generate email content
        subject = f"{template.name} - {execution.report_date.strftime('%B %d, %Y')}"
        body = self.generate_report_html(report_data, template.name, execution.report_date)
        
        success_count = 0
        for user_id in recipients:
            user = User.query.get(user_id)
            if user and user.email:
                # Create email notification record
                notification = EmailNotification(
                    id=str(uuid.uuid4()),
                    recipient_email=user.email,
                    subject=subject,
                    body=body,
                    report_execution_id=report_execution_id,
                    status='pending'
                )
                db.session.add(notification)
                
                # Send email
                if self.send_email(user.email, subject, body):
                    notification.status = 'sent'
                    notification.sent_at = datetime.utcnow()
                    success_count += 1
                else:
                    notification.status = 'failed'
        
        db.session.commit()
        return success_count
    
    def generate_report_html(self, report_data, report_name, report_date):
        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 5px; }}
                .metric {{ display: inline-block; margin: 10px; padding: 15px; background-color: #e9ecef; border-radius: 5px; }}
                .metric-value {{ font-size: 24px; font-weight: bold; color: #007bff; }}
                .metric-label {{ font-size: 14px; color: #6c757d; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
                th {{ background-color: #f8f9fa; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>{report_name}</h2>
                <p>Report Date: {report_date.strftime('%B %d, %Y')}</p>
            </div>
            
            <h3>Key Metrics</h3>
            <div class="metric">
                <div class="metric-value">{report_data.get('total_accounts', 0)}</div>
                <div class="metric-label">Total Accounts</div>
            </div>
            <div class="metric">
                <div class="metric-value">KES {report_data.get('total_balance', 0):,.2f}</div>
                <div class="metric-label">Outstanding Balance</div>
            </div>
            <div class="metric">
                <div class="metric-value">{report_data.get('collections_today', 0)}</div>
                <div class="metric-label">Collections Today</div>
            </div>
            <div class="metric">
                <div class="metric-value">KES {report_data.get('amount_collected_today', 0):,.2f}</div>
                <div class="metric-label">Amount Collected Today</div>
            </div>
            
            <h3>Officer Performance</h3>
            <table>
                <tr>
                    <th>Officer</th>
                    <th>Accounts</th>
                    <th>Collections</th>
                    <th>Amount</th>
                    <th>PTPs</th>
                </tr>
        """
        
        for officer in report_data.get('officer_performance', []):
            html += f"""
                <tr>
                    <td>{officer.get('name', 'N/A')}</td>
                    <td>{officer.get('accounts', 0)}</td>
                    <td>{officer.get('collections', 0)}</td>
                    <td>KES {officer.get('amount', 0):,.2f}</td>
                    <td>{officer.get('ptps', 0)}</td>
                </tr>
            """
        
        html += """
            </table>
            
            <p><small>This is an automated report from the Collections Management System.</small></p>
        </body>
        </html>
        """
        
        return html

email_service = EmailService()