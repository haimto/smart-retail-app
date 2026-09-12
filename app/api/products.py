from flask import Blueprint, request, jsonify
from app.models import db
from app.models.product import Product
from app.models.restock import RestockLog

products_bp = Blueprint('products', __name__, url_prefix='/api/products')

@products_bp.route('', methods=['GET'])
def get_products():
    products = db.session.execute(db.select(Product)).scalars().all()
    return jsonify([p.to_dict() for p in products]), 200

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = db.get_or_404(Product, product_id)
    return jsonify(product.to_dict()), 200

@products_bp.route('', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data or 'name' not in data or 'sku' not in data:
        return jsonify({'error': 'Missing required fields (name, sku)'}), 400
    
    existing = db.session.execute(db.select(Product).filter_by(sku=data['sku'])).scalar_one_or_none()
    if existing:
        return jsonify({'error': 'Product with this SKU already exists'}), 409

    new_product = Product(
        name=data['name'],
        sku=data['sku'],
        stock_level=data.get('stock_level', 0),
        threshold=data.get('threshold', 10)
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = db.get_or_404(Product, product_id)
    data = request.get_json()
    if 'name' in data: product.name = data['name']
    if 'stock_level' in data: product.stock_level = data['stock_level']
    if 'threshold' in data: product.threshold = data['threshold']
    db.session.commit()
    return jsonify(product.to_dict()), 200

@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = db.get_or_404(Product, product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': f'Product {product_id} deleted successfully'}), 200

# --- NEW DAY 5 ENDPOINTS ---

@products_bp.route('/<int:product_id>/restock', methods=['POST'])
def restock_product(product_id):
    product = db.get_or_404(Product, product_id)
    data = request.get_json()
    
    if not data or 'quantity' not in data or data['quantity'] <= 0:
        return jsonify({'error': 'Must provide a positive quantity'}), 400

    quantity = data['quantity']
    product.stock_level += quantity  # Update current stock
    
    # Audit log the transaction
    log = RestockLog(product_id=product.id, quantity=quantity)
    db.session.add(log)
    db.session.commit()
    
    return jsonify({
        'message': 'Restock successful',
        'new_stock_level': product.stock_level
    }), 200

@products_bp.route('/low-stock', methods=['GET'])
def get_low_stock():
    # Query products where current stock is strictly less than the threshold
    low_stock = db.session.execute(
        db.select(Product).filter(Product.stock_level < Product.threshold)
    ).scalars().all()
    return jsonify([p.to_dict() for p in low_stock]), 200

@products_bp.route('/analytics', methods=['GET'])
def get_analytics():
    total_products = db.session.scalar(db.select(db.func.count(Product.id))) or 0
    total_stock = db.session.scalar(db.select(db.func.sum(Product.stock_level))) or 0
    low_stock_count = db.session.scalar(
        db.select(db.func.count(Product.id)).filter(Product.stock_level < Product.threshold)
    ) or 0

    return jsonify({
        'total_products_tracked': total_products,
        'total_items_in_stock': int(total_stock),
        'items_needing_restock': low_stock_count
    }), 200
