from app import db
from datetime import datetime


class RestaurantCategory(db.Model):
    __tablename__ = 'restaurant_categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    icon = db.Column(db.String(100), nullable=True)   # emoji or icon class
    image_url = db.Column(db.String(255), nullable=True)
    display_order = db.Column(db.Integer, default=0)
    restaurants = db.relationship('Restaurant', backref='category', lazy='dynamic')

    def __repr__(self):
        return f'<RestaurantCategory {self.name}>'


class Restaurant(db.Model):
    __tablename__ = 'restaurants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('restaurant_categories.id'), nullable=True)
    cuisine_type = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False, default='Hyderabad')
    phone = db.Column(db.String(15), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    cover_image_url = db.Column(db.String(255), nullable=True)
    rating = db.Column(db.Float, default=4.0)
    total_reviews = db.Column(db.Integer, default=0)
    delivery_time = db.Column(db.Integer, default=30)   # minutes
    min_order = db.Column(db.Float, default=100.0)
    delivery_fee = db.Column(db.Float, default=30.0)
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    is_veg_only = db.Column(db.Boolean, default=False)
    opening_time = db.Column(db.Time, nullable=True)
    closing_time = db.Column(db.Time, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    menu_categories = db.relationship('MenuCategory', backref='restaurant', lazy='dynamic', cascade='all, delete-orphan')
    menu_items = db.relationship('MenuItem', backref='restaurant', lazy='dynamic', cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='restaurant', lazy='dynamic')
    operating_hours = db.relationship('OperatingHours', backref='restaurant', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='restaurant', lazy='dynamic')

    def rating_stars(self):
        return round(self.rating * 2) / 2

    def is_open(self):
        from datetime import datetime as dt
        now = dt.now().time()
        if self.opening_time and self.closing_time:
            return self.opening_time <= now <= self.closing_time
        return True

    def update_rating(self):
        from app.models.review import Review
        reviews = Review.query.filter_by(restaurant_id=self.id).all()
        if reviews:
            self.rating = sum(r.rating for r in reviews) / len(reviews)
            self.total_reviews = len(reviews)
        db.session.commit()

    def __repr__(self):
        return f'<Restaurant {self.name}>'


class OperatingHours(db.Model):
    __tablename__ = 'operating_hours'

    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)  # 0=Mon, 6=Sun
    open_time = db.Column(db.Time, nullable=False)
    close_time = db.Column(db.Time, nullable=False)
    is_closed = db.Column(db.Boolean, default=False)

    DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    @property
    def day_name(self):
        return self.DAYS[self.day_of_week]

    def __repr__(self):
        return f'<OperatingHours {self.day_name}: {self.open_time}-{self.close_time}>'
