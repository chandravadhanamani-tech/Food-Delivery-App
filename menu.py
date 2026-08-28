from app import db
from datetime import datetime


class MenuCategory(db.Model):
    __tablename__ = 'menu_categories'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    items = db.relationship('MenuItem', backref='menu_category', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<MenuCategory {self.name}>'


class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('menu_categories.id'), nullable=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discounted_price = db.Column(db.Numeric(10, 2), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    is_veg = db.Column(db.Boolean, default=True)
    is_available = db.Column(db.Boolean, default=True)
    is_popular = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    spice_level = db.Column(db.Enum('mild', 'medium', 'hot', 'extra_hot'), default='medium')
    calories = db.Column(db.Integer, nullable=True)
    preparation_time = db.Column(db.Integer, default=15)  # minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    order_items = db.relationship('OrderItem', backref='menu_item', lazy='dynamic')

    @property
    def effective_price(self):
        return self.discounted_price if self.discounted_price else self.price

    @property
    def discount_percent(self):
        if self.discounted_price and self.price > 0:
            return int(((self.price - self.discounted_price) / self.price) * 100)
        return 0

    def __repr__(self):
        return f'<MenuItem {self.name} ₹{self.price}>'
