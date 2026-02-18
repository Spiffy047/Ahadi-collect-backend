#!/usr/bin/env python3
"""
Alert Scheduler - Runs daily checks for payment alerts and notifications
"""

import schedule
import time
from datetime import datetime
from app import app
from alert_service import alert_service

def run_daily_alerts():
    """Run daily alert checks within Flask app context"""
    with app.app_context():
        try:
            print(f"[{datetime.now()}] Starting daily alert checks...")
            alert_service.run_daily_checks()
            print(f"[{datetime.now()}] Daily alert checks completed successfully")
        except Exception as e:
            print(f"[{datetime.now()}] Error running daily alert checks: {str(e)}")

def main():
    """Main scheduler function"""
    print("Alert Scheduler started...")
    
    # Schedule daily checks at 9:00 AM
    schedule.every().day.at("09:00").do(run_daily_alerts)
    
    # Also run checks every 4 hours during business hours
    schedule.every(4).hours.do(run_daily_alerts)
    
    # Run initial check
    run_daily_alerts()
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == '__main__':
    main()