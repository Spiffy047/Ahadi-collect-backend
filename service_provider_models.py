# Add to models.py - Service Provider for Geo Mapping
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
    current_status = db.Column(db.Enum('available', 'repossessed', 'sold', 'under_valuation', 'disputed'), default='available')
    location_address = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    assigned_provider_id = db.Column(db.String(50), db.ForeignKey('service_provider.id'))
    registration_number = db.Column(db.String(100))  # For vehicles/machinery
    title_deed_number = db.Column(db.String(100))  # For land/property
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    account = db.relationship('Account')
    assigned_provider = db.relationship('ServiceProvider')