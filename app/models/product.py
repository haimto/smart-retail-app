from app.models import db
from datetime import datetime, timezone

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True, nullable=False)
    stock_level = db.Column(db.Integer, default=0)
    threshold = db.Column(db.Integer, default=10) # Used for low-stock alerts
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "sku": self.sku,
            "stock_level": self.stock_level,
            "threshold": self.threshold
        }
