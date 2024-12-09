from flask import Blueprint, request
from application.models import Institution, db
from application.utils import ResponseHelper
import uuid

institution_bp = Blueprint('institution', __name__, url_prefix='/institutions')

# Create Institution
@institution_bp.route('/', methods=['POST'])
def create_institution():
    """Create a new institution."""
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    if not name or not email:
        return ResponseHelper.default_response("Name and email are required", 400)

    # Check if institution already exists
    if Institution.query.filter_by(email=email).first():
        return ResponseHelper.default_response("Institution with this email already exists", 400)

    # Create institution
    institution = Institution(
        institutionID=str(uuid.uuid4()),
        name=name,
        email=email
    )
    db.session.add(institution)
    db.session.commit()

    return ResponseHelper.default_response(
        "Institution created successfully",
        201,
        {"id": institution.institutionID}
    )

# Get All Institutions
@institution_bp.route('/', methods=['GET'])
def get_institutions():
    """Retrieve all institutions."""
    institutions = Institution.query.all()
    data = [
        {
            "id": institution.institutionID,
            "name": institution.name,
            "email": institution.email,
            "subscriptionStatus": institution.subscriptionStatus
        }
        for institution in institutions
    ]

    return ResponseHelper.default_response(
        "Institutions retrieved successfully",
        200,
        {"institutions": data}
    )

# Get Institution by ID
@institution_bp.route('/<string:id>', methods=['GET'])
def get_institution(id):
    """Retrieve institution details by ID."""
    institution = Institution.query.filter_by(institutionID=id).first()

    if not institution:
        return ResponseHelper.default_response("Institution not found", 404)

    data = {
        "id": institution.institutionID,
        "name": institution.name,
        "email": institution.email,
        "subscriptionStatus": institution.subscriptionStatus
    }

    return ResponseHelper.default_response(
        "Institution details retrieved successfully",
        200,
        data
    )
