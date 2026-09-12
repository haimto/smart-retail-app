from flask import Flask, jsonify
from app.config import config_by_name
from app.models import db

def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    # Initialize the database with the app
    db.init_app(app)

    # Register Blueprints
    from app.api.products import products_bp
    app.register_blueprint(products_bp)
    
    from app.api.restocks import restocks_bp
    app.register_blueprint(restocks_bp)

    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "healthy",
            "service": "smart-retail-api"
        }), 200

    return app
