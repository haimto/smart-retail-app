from app import create_app
from app.models import db
from app.models.product import Product
from app.models.restock import RestockLog

# Create the Flask application instance
app = create_app()

# Create the tables within the application context
with app.app_context():
    db.create_all()
    print("Successfully generated PostgreSQL tables!")
