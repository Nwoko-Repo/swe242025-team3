from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from application.models import Product, db
from application.utils import ResponseHelper
import datetime
import uuid

product_bp = Blueprint('product', __name__, url_prefix='/products')

# Add Product (Admin-only)
@product_bp.route('/', methods=['POST'])
@jwt_required()
def add_product():
    current_user = get_jwt_identity()
    if current_user['role'] != 'administrator':
        return ResponseHelper.default_response("Permission denied", 403)

    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    stock_quantity = data.get('stockQuantity')
    category = data.get('category')

    if not name or not price:
        return ResponseHelper.default_response("Name and Price are required fields", 400)

    product = Product(
        productID=f"prod-{uuid.uuid4()}",
        name=name,
        description=description,
        price=price,
        stockQuantity=stock_quantity,
        category=category
    )
    db.session.add(product)
    db.session.commit()

    return ResponseHelper.default_response(
        "Product added successfully",
        201,
        {"id": product.productID}
    )


# Get Product List
@product_bp.route('/', methods=['GET'])
def get_products():
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 10, type=int)

    products = Product.query.paginate(page=page, per_page=size)
    data = [
        {
            "id": product.productID,
            "name": product.name,
            "price": product.price,
            "stockQuantity": product.stockQuantity,
            "category": product.category
        }
        for product in products.items
    ]

    return ResponseHelper.default_response(
        "Products fetched successfully",
        200,
        {
            "data": data,
            "pagination": {
                "currentPage": products.page,
                "totalPages": products.pages,
                "totalItems": products.total
            }
        }
    )


# Get Product Details
@product_bp.route('/<string:product_id>', methods=['GET'])
def get_product_details(product_id):
    product = Product.query.filter_by(productID=product_id).first()

    if not product:
        return ResponseHelper.default_response("Product not found", 404)

    return ResponseHelper.default_response(
        "Product details fetched successfully",
        200,
        {
            "id": product.productID,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "stockQuantity": product.stockQuantity,
            "category": product.category
        }
    )


# Update Product (Admin-only)
@product_bp.route('/<string:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'administrator':
        return ResponseHelper.default_response("Permission denied", 403)

    product = Product.query.filter_by(productID=product_id).first()
    if not product:
        return ResponseHelper.default_response("Product not found", 404)

    data = request.get_json()
    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stockQuantity = data.get('stockQuantity', product.stockQuantity)
    product.category = data.get('category', product.category)
    product.updatedDate = datetime.datetime.utcnow()

    db.session.commit()

    return ResponseHelper.default_response("Product updated successfully", 200)


# Delete Product (Admin-only)
@product_bp.route('/<string:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    current_user = get_jwt_identity()
    if current_user['role'] != 'administrator':
        return ResponseHelper.default_response("Permission denied", 403)

    product = Product.query.filter_by(productID=product_id).first()
    if not product:
        return ResponseHelper.default_response("Product not found", 404)

    db.session.delete(product)
    db.session.commit()

    return ResponseHelper.default_response("Product deleted successfully", 200)
