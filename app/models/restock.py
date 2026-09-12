from app.models import db
from datetime import datetime, timezone

class RestockLog(db.Model):
    __tablename__ = 'restock_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Establish a relationship to query a product's history easily
    product = db.relationship('Product', backref=db.backref('restock_logs', lazy=True))

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "timestamp": self.timestamp.isoformat()
        }
