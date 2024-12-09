from app import db
from datetime import datetime

# Mixin for adding timestamps
class TimestampMixin:
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    updatedDate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Customer Model
class Customer(TimestampMixin,db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.String, nullable=False, unique=True)  # E-commerce system's customer ID
    stripe_customer_id = db.Column(db.String, nullable=False, unique=True)  # Stripe's customer ID (authToken)
    email = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=True)

    # Relationships
    payments = db.relationship('Payment', backref='customer', lazy=True)

# Payment Model
class Payment(TimestampMixin,db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.String, primary_key=True)  # Unique identifier for the payment
    customer_id = db.Column(db.String, db.ForeignKey('customers.customer_id'), nullable=False)
    stripe_payment_id = db.Column(db.String, nullable=False)  # Stripe's payment ID
    stripe_session_id = db.Column(db.String, nullable=False)  # Stripe Checkout session ID
    order_id = db.Column(db.String, nullable=False)  # Order ID from the e-commerce service
    amount = db.Column(db.Float, nullable=False)  # Payment amount
    status = db.Column(db.String, default="pending")  # Payment status

# Institution Model
class Institution(TimestampMixin, db.Model):
    __tablename__ = 'institution'
    institutionID = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    subscriptionStatus = db.Column(db.String, default='active')

    # Relationships
    api_access = db.relationship('APIAccess', backref='institution', lazy=True)

# APIAccess Model
class APIAccess(TimestampMixin, db.Model):
    __tablename__ = 'api_access'
    accessID = db.Column(db.String, primary_key=True)
    token = db.Column(db.String, nullable=False)
    expirationDate = db.Column(db.DateTime, nullable=False)

    # Foreign Keys
    institutionID = db.Column(db.String, db.ForeignKey('institution.institutionID'), nullable=False)

# Observation Model
class Observation(TimestampMixin, db.Model):
    __tablename__ = 'observation'
    observationID = db.Column(db.String, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    windSpeed = db.Column(db.Float, nullable=True)
    precipitation = db.Column(db.Float, nullable=True)
    locationCoordinates = db.Column(db.String, nullable=True)

    # Foreign Keys
    deviceID = db.Column(db.String, db.ForeignKey('iot_device.deviceID'), nullable=False)

# IoTDevice Model
class IoTDevice(TimestampMixin, db.Model):
    __tablename__ = 'iot_device'
    deviceID = db.Column(db.String, primary_key=True)
    location = db.Column(db.String, nullable=False)
    batteryStatus = db.Column(db.String, nullable=False)
    transmissionInterval = db.Column(db.Integer, nullable=False)

    # Relationships
    observations = db.relationship('Observation', backref='iot_device', lazy=True)

# Administrator Model
class Administrator(TimestampMixin, db.Model):
    __tablename__ = 'administrator'
    adminID = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    permissions = db.Column(db.String, nullable=False)

    # Relationships
    audit_logs = db.relationship('AuditLog', backref='administrator', lazy=True)

# AuditLog Model
class AuditLog(TimestampMixin, db.Model):
    __tablename__ = 'audit_log'
    logID = db.Column(db.String, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    action = db.Column(db.String, nullable=False)

    # Foreign Keys
    adminID = db.Column(db.String, db.ForeignKey('administrator.adminID'), nullable=False)

