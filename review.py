from app import db
from datetime import datetime


class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=True, unique=True)
    rating = db.Column(db.Integer, nullable=False)   # 1–5
    comment = db.Column(db.Text, nullable=True)
    food_rating = db.Column(db.Integer, nullable=True)
    delivery_rating = db.Column(db.Integer, nullable=True)
    is_verified = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def star_range(self):
        return range(1, 6)

    def __repr__(self):
        return f'<Review {self.rating}★ for restaurant {self.restaurant_id}>'
