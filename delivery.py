from app import db
from datetime import datetime


class DeliveryPartner(db.Model):
    __tablename__ = 'delivery_partners'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    vehicle_type = db.Column(db.Enum('bicycle', 'motorcycle', 'car'), default='motorcycle')
    vehicle_number = db.Column(db.String(20), nullable=True)
    license_number = db.Column(db.String(30), nullable=True)
    is_available = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    current_location = db.Column(db.String(255), nullable=True)
    total_deliveries = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=5.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    assignments = db.relationship('DeliveryAssignment', backref='partner', lazy='dynamic')

    def __repr__(self):
        return f'<DeliveryPartner user_id={self.user_id}>'


class DeliveryAssignment(db.Model):
    __tablename__ = 'delivery_assignments'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), unique=True, nullable=False)
    partner_id = db.Column(db.Integer, db.ForeignKey('delivery_partners.id'), nullable=False)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
    picked_up_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    delivery_notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<DeliveryAssignment order={self.order_id} partner={self.partner_id}>'
