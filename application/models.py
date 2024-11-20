from app import db
from datetime import datetime

# Mixin for adding timestamps
class TimestampMixin:
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    updatedDate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Customer Model
class Customer(TimestampMixin, db.Model):
    __tablename__ = 'customer'
    customerID = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=True)
    accountStatus = db.Column(db.String, default='active')

    # Relationships
    orders = db.relationship('Order', backref='customer', lazy=True)

# Product Model
class Product(TimestampMixin, db.Model):
    __tablename__ = 'product'
    productID = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stockQuantity = db.Column(db.Integer, default=0)
    category = db.Column(db.String, nullable=True)

# Order Model
class Order(TimestampMixin, db.Model):
    __tablename__ = 'order'
    orderID = db.Column(db.String, primary_key=True)
    orderDate = db.Column(db.DateTime, default=datetime.utcnow)
    totalAmount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String, default='pending')

    # Foreign Keys
    customerID = db.Column(db.String, db.ForeignKey('customer.customerID'), nullable=False)

    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True)

# OrderItem Model
class OrderItem(TimestampMixin, db.Model):
    __tablename__ = 'order_item'
    orderItemID = db.Column(db.String, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)

    # Foreign Keys
    productID = db.Column(db.String, db.ForeignKey('product.productID'), nullable=False)
    orderID = db.Column(db.String, db.ForeignKey('order.orderID'), nullable=False)

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
