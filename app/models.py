from app.extensions import db
from datetime import datetime, timezone


class Product(db.Model):
    '''
        Product Schema
    '''
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(128), nullable=False)
    sku = db.Column(db.String(128), unique=True, nullable=False)

    created_at = db.Column(
        db.DateTime, default=datetime.now().astimezone(timezone.utc))
    updated_at = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now().astimezone(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
            "sku": self.sku
        }
