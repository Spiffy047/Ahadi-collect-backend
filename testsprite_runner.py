#!/usr/bin/env python3
"""
TestSprite Integration for Collections Management System
Automated end-to-end testing using TestSprite API
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

class TestSpriteRunner:
    def __init__(self):
        self.api_key = os.getenv('TESTSPRITE_API_KEY')
        self.base_url = "https://api.testsprite.com/v1"
        self.app_url = "http://localhost:5000"
        
    def run_tests(self):
        """Execute automated tests via TestSprite"""
        
        test_suite = {
            "name": "Collections Management System - E2E Tests",
            "base_url": self.app_url,
            "tests": [
                {
                    "name": "User Login - Administrator",
                    "steps": [
                        {
                            "action": "navigate",
                            "url": f"{self.app_url}/login"
                        },
                        {
                            "action": "fill",
                            "selector": "input[type='email']",
                            "value": "testsprite@collections.com"
                        },
                        {
                            "action": "fill",
                            "selector": "input[type='password']",
                            "value": "testsprite"
                        },
                        {
                            "action": "click",
                            "selector": "button[type='submit']"
                        },
                        {
                            "action": "wait",
                            "selector": ".dashboard"
                        }
                    ],
                    "assertions": [
                        {
                            "type": "url_contains",
                            "value": "/dashboard"
                        }
                    ]
                },
                {
                    "name": "View Accounts List",
                    "steps": [
                        {
                            "action": "click",
                            "selector": "a[href='/accounts']"
                        },
                        {
                            "action": "wait",
                            "selector": ".accounts-table"
                        }
                    ],
                    "assertions": [
                        {
                            "type": "element_exists",
                            "selector": ".accounts-table"
                        }
                    ]
                },
                {
                    "name": "Create Payment",
                    "steps": [
                        {
                            "action": "navigate",
                            "url": f"{self.app_url}/accounts"
                        },
                        {
                            "action": "click",
                            "selector": ".account-row:first-child"
                        },
                        {
                            "action": "click",
                            "selector": "button:contains('Record Payment')"
                        },
                        {
                            "action": "fill",
                            "selector": "input[name='amount']",
                            "value": "10000"
                        },
                        {
                            "action": "select",
                            "selector": "select[name='payment_method']",
                            "value": "mpesa"
                        },
                        {
                            "action": "click",
                            "selector": "button[type='submit']"
                        }
                    ],
                    "assertions": [
                        {
                            "type": "text_contains",
                            "value": "Payment recorded successfully"
                        }
                    ]
                },
                {
                    "name": "View Analytics Dashboard",
                    "steps": [
                        {
                            "action": "navigate",
                            "url": f"{self.app_url}/reports/advanced-reports"
                        },
                        {
                            "action": "wait",
                            "selector": ".analytics-dashboard"
                        }
                    ],
                    "assertions": [
                        {
                            "type": "element_exists",
                            "selector": ".collections-trend-chart"
                        },
                        {
                            "type": "element_exists",
                            "selector": ".legal-metrics"
                        }
                    ]
                }
            ]
        }
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        print("🧪 Running TestSprite automated tests...")
        
        try:
            response = requests.post(
                f"{self.base_url}/test-suites/run",
                headers=headers,
                json=test_suite
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Tests completed: {result.get('passed', 0)}/{result.get('total', 0)} passed")
                return result
            else:
                print(f"❌ TestSprite API error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error running tests: {str(e)}")
            return None

if __name__ == '__main__':
    runner = TestSpriteRunner()
    runner.run_tests()
