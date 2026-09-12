from flask import Blueprint, jsonify
from app.models import db
from app.models.restock import RestockLog

restocks_bp = Blueprint('restocks', __name__, url_prefix='/api/restocks')

@restocks_bp.route('', methods=['GET'])
def get_restock_history():
    # Fetch logs descending by timestamp
    logs = db.session.execute(
        db.select(RestockLog).order_by(RestockLog.timestamp.desc())
    ).scalars().all()
    return jsonify([log.to_dict() for log in logs]), 200
