# DM9 Debt Collections System - Backend

Flask backend for the DM9 Debt Collections System, configured for Kenyan market with KES currency support.

## Features

- **Authentication**: JWT-based authentication with DM9 SOAP integration
- **Consumer Management**: CRUD operations for consumer data
- **Account Management**: Account tracking and balance management
- **Payment Processing**: ACH and card payment processing
- **Currency Support**: Full Kenyan Shilling (KES) formatting and calculations
- **API Integration**: Ready for DM9 SOAP service integration

## Setup

### Prerequisites
- Python 3.8+
- DM9 SOAP API access

### Installation

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.example .env
# Edit .env with your DM9 credentials
```

4. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Consumers
- `GET /api/consumers` - List consumers (paginated)
- `GET /api/consumers/{id}` - Get consumer details

### Accounts
- `GET /api/accounts` - List accounts (paginated)
- `GET /api/accounts/{id}` - Get account details

### Payments
- `GET /api/payments` - Payment history
- `POST /api/payments/ach` - Process ACH payment
- `POST /api/payments/card` - Process card payment

### Dashboard
- `GET /api/reports/dashboard` - Dashboard statistics

## Currency Configuration

All monetary values are handled in Kenyan Shillings (KES):
- Currency code: `KES`
- Symbol: `KSh`
- Format: `KSh 1,234.56`

## DM9 Integration

To connect to DM9 SOAP services, update the following in your `.env`:

```env
DM9_SOAP_URL=http://your-dm9-server/services/
DM9_USERNAME=your_username
DM9_PASSWORD=your_password
```

Example DM9 SOAP client integration:

```python
from zeep import Client

class DM9Client:
    def __init__(self):
        self.wsdl_url = app.config['DM9_SOAP_URL']
        self.username = app.config['DM9_USERNAME']
        self.password = app.config['DM9_PASSWORD']
        self.client = Client(self.wsdl_url)
    
    def search_consumers(self, params):
        return self.client.service.SearchConsumers(params)
```

## Kenyan Banking Integration

For M-Pesa and local banking integration, configure:

```env
MPESA_CONSUMER_KEY=your_key
MPESA_CONSUMER_SECRET=your_secret
MPESA_SHORTCODE=your_shortcode
```

## Development

The backend is currently using mock data. To connect to real DM9 services:

1. Implement DM9 SOAP client in `dm9_client.py`
2. Replace mock responses with actual DM9 API calls
3. Add proper error handling and validation
4. Implement authentication middleware

## Production Deployment

1. Set `FLASK_ENV=production`
2. Use a production WSGI server (Gunicorn)
3. Configure reverse proxy (Nginx)
4. Set up SSL certificates
5. Configure firewall and security groups# Ahadi-collect-backend
