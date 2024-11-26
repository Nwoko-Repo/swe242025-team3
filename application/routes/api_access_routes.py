from flask import Blueprint, request
from application.models import APIAccess, Institution, db
from application.utils import ResponseHelper
from datetime import datetime, timedelta
import uuid

api_access_bp = Blueprint('api_access', __name__, url_prefix='/api-access')

# Generate API Token
@api_access_bp.route('/', methods=['POST'])
def generate_api_token():
    """Generate a new API token for an institution."""
    data = request.get_json()
    institution_id = data.get('institutionID')
    expiration_days = data.get('expirationDays', 30)

    # Validate institution
    institution = Institution.query.filter_by(institutionID=institution_id).first()
    if not institution:
        return ResponseHelper.default_response("Institution not found", 404)

    # Generate API token
    token = str(uuid.uuid4())
    expiration_date = datetime.utcnow() + timedelta(days=expiration_days)

    api_access = APIAccess(
        accessID=str(uuid.uuid4()),
        token=token,
        expirationDate=expiration_date,
        institutionID=institution_id
    )
    db.session.add(api_access)
    db.session.commit()

    return ResponseHelper.default_response(
        "API token generated successfully",
        201,
        {
            "accessID": api_access.accessID,
            "token": api_access.token,
            "expirationDate": expiration_date.isoformat()
        }
    )

# Get All API Tokens
@api_access_bp.route('/', methods=['GET'])
def get_api_tokens():
    """Retrieve all API tokens for an institution."""
    institution_id = request.args.get('institutionID')

    # Validate institution
    institution = Institution.query.filter_by(institutionID=institution_id).first()
    if not institution:
        return ResponseHelper.default_response("Institution not found", 404)

    # Retrieve tokens
    tokens = APIAccess.query.filter_by(institutionID=institution_id).all()
    data = [
        {
            "accessID": token.accessID,
            "token": token.token,
            "expirationDate": token.expirationDate.isoformat()
        }
        for token in tokens
    ]

    return ResponseHelper.default_response(
        "API tokens retrieved successfully",
        200,
        {"tokens": data}
    )

# Revoke API Token
@api_access_bp.route('/<string:access_id>', methods=['DELETE'])
def revoke_api_token(access_id):
    """Revoke an API token by its access ID."""
    api_access = APIAccess.query.filter_by(accessID=access_id).first()

    if not api_access:
        return ResponseHelper.default_response("API token not found", 404)

    db.session.delete(api_access)
    db.session.commit()

    return ResponseHelper.default_response("API token revoked successfully", 200)
