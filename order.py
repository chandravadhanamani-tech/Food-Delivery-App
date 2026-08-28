from app import db
from datetime import datetime


class Order(db.Model):
    __tablename__ = 'orders'

    STATUS_PLACED = 'placed'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_PREPARING = 'preparing'
    STATUS_OUT_FOR_DELIVERY = 'out_for_delivery'
    STATUS_DELIVERED = 'delivered'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        STATUS_PLACED, STATUS_CONFIRMED, STATUS_PREPARING,
        STATUS_OUT_FOR_DELIVERY, STATUS_DELIVERED, STATUS_CANCELLED
    ]

    PAYMENT_COD = 'cod'
    PAYMENT_RAZORPAY = 'razorpay'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    status = db.Column(
        db.Enum('placed', 'confirmed', 'preparing', 'out_for_delivery', 'delivered', 'cancelled'),
        default='placed', nullable=False
    )
    # Delivery address (snapshot at order time)
    delivery_address = db.Column(db.Text, nullable=False)
    delivery_name = db.Column(db.String(100), nullable=False)
    delivery_phone = db.Column(db.String(15), nullable=False)

    # Pricing
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    delivery_fee = db.Column(db.Numeric(10, 2), default=30.00)
    tax = db.Column(db.Numeric(10, 2), default=0.00)
    discount = db.Column(db.Numeric(10, 2), default=0.00)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)

    # Payment
    payment_method = db.Column(db.Enum('cod', 'razorpay'), default='cod')
    payment_status = db.Column(db.Enum('pending', 'paid', 'failed', 'refunded'), default='pending')
    razorpay_order_id = db.Column(db.String(100), nullable=True)
    razorpay_payment_id = db.Column(db.String(100), nullable=True)

    # Notes
    special_instructions = db.Column(db.Text, nullable=True)
    estimated_delivery_time = db.Column(db.Integer, default=45)  # minutes

    # Timestamps
    placed_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime, nullable=True)
    preparing_at = db.Column(db.DateTime, nullable=True)
    out_for_delivery_at = db.Column(db.DateTime, nullable=True)
    delivered_at = db.Column(db.DateTime, nullable=True)
    cancelled_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')
    delivery_assignment = db.relationship('DeliveryAssignment', backref='order', uselist=False)
    review = db.relationship('Review', backref='order', uselist=False)

    STATUS_LABELS = {
        'placed': ('Order Placed', 'bi-check-circle', 'warning'),
        'confirmed': ('Confirmed', 'bi-check-circle-fill', 'info'),
        'preparing': ('Preparing', 'bi-fire', 'primary'),
        'out_for_delivery': ('Out for Delivery', 'bi-bicycle', 'success'),
        'delivered': ('Delivered', 'bi-bag-check-fill', 'success'),
        'cancelled': ('Cancelled', 'bi-x-circle-fill', 'danger'),
    }

    def get_status_info(self):
        return self.STATUS_LABELS.get(self.status, ('Unknown', 'bi-question', 'secondary'))

    def status_timeline(self):
        steps = [
            ('placed', 'Order Placed', 'bi-receipt'),
            ('confirmed', 'Confirmed', 'bi-check-circle'),
            ('preparing', 'Preparing', 'bi-fire'),
            ('out_for_delivery', 'Out for Delivery', 'bi-bicycle'),
            ('delivered', 'Delivered', 'bi-bag-check-fill'),
        ]
        flow = [s[0] for s in steps]
        current_idx = flow.index(self.status) if self.status in flow else -1
        result = []
        for i, (status, label, icon) in enumerate(steps):
            if i < current_idx:
                state = 'completed'
            elif i == current_idx:
                state = 'active'
            else:
                state = 'pending'
            result.append({'status': status, 'label': label, 'icon': icon, 'state': state})
        return result

    def update_status(self, new_status):
        self.status = new_status
        now = datetime.utcnow()
        if new_status == 'confirmed':
            self.confirmed_at = now
        elif new_status == 'preparing':
            self.preparing_at = now
        elif new_status == 'out_for_delivery':
            self.out_for_delivery_at = now
        elif new_status == 'delivered':
            self.delivered_at = now
            if self.payment_method == 'cod':
                self.payment_status = 'paid'
        elif new_status == 'cancelled':
            self.cancelled_at = now

    @staticmethod
    def generate_order_number():
        import random
        import string
        prefix = 'FD'
        suffix = ''.join(random.choices(string.digits, k=8))
        return f"{prefix}{suffix}"

    def __repr__(self):
        return f'<Order {self.order_number} - {self.status}>'


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    special_request = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f'<OrderItem {self.menu_item_id} x{self.quantity}>'
