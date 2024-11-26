from flask import Blueprint, request
from application.models import Observation, IoTDevice, APIAccess, db
from application.utils import ResponseHelper
from datetime import datetime, timedelta

observations_bp = Blueprint('observations', __name__, url_prefix='/observations')

# Helper: Validate API Token
def validate_api_token(token):
    """Check if the API token is valid and not expired."""
    api_access = APIAccess.query.filter_by(token=token).first()
    if not api_access:
        return False, "Invalid API token."
    if api_access.expirationDate < datetime.utcnow():
        return False, "API token has expired."
    return True, api_access.institutionID

# Add Observation
@observations_bp.route('/', methods=['POST'])
def add_observation():
    """Add a new observation from an IoT device."""
    data = request.get_json()

    # Validate device
    device_id = data.get("deviceID")
    device = IoTDevice.query.filter_by(deviceID=device_id).first()
    if not device:
        return ResponseHelper.default_response("IoT Device not registered", 404)

    # Create observation
    observation = Observation(
        observationID=f"obs-{datetime.utcnow().timestamp()}",
        timestamp=datetime.fromisoformat(data.get("timestamp")),
        temperature=data.get("temperature"),
        humidity=data.get("humidity"),
        windSpeed=data.get("windSpeed"),
        precipitation=data.get("precipitation"),
        locationCoordinates=data.get("locationCoordinates"),
        deviceID=device_id
    )
    db.session.add(observation)
    db.session.commit()

    return ResponseHelper.default_response(
        "Observation added successfully",
        201,
        {"observationID": observation.observationID}
    )

# Get Observations
@observations_bp.route('/', methods=['GET'])
def get_observations():
    """Retrieve observations with optional filters and validate API access."""
    token = request.headers.get("Authorization")  # API token should be sent in the header

    # Validate API token
    is_valid, message_or_institution_id = validate_api_token(token)
    if not is_valid:
        return ResponseHelper.default_response(message_or_institution_id, 403)

    # Apply filters
    device_id = request.args.get("deviceID")
    start_date = request.args.get("startDate")
    end_date = request.args.get("endDate")

    query = Observation.query
    if device_id:
        query = query.filter_by(deviceID=device_id)
    if start_date:
        query = query.filter(Observation.timestamp >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Observation.timestamp <= datetime.fromisoformat(end_date))

    # Retrieve observations
    observations = query.all()
    data = [
        {
            "observationID": obs.observationID,
            "timestamp": obs.timestamp.isoformat(),
            "temperature": obs.temperature,
            "humidity": obs.humidity,
            "windSpeed": obs.windSpeed,
            "precipitation": obs.precipitation,
            "locationCoordinates": obs.locationCoordinates,
            "deviceID": obs.deviceID
        }
        for obs in observations
    ]

    return ResponseHelper.default_response(
        "Observations retrieved successfully",
        200,
        {"observations": data}
    )

# Mock Observations (Updated for API validation)
@observations_bp.route('/mock', methods=['GET'])
def mock_observations():
    """Generate mock observations for all IoT devices."""
    token = request.headers.get("Authorization")  # API token should be sent in the header

    # Validate API token
    is_valid, message_or_institution_id = validate_api_token(token)
    if not is_valid:
        return ResponseHelper.default_response(message_or_institution_id, 403)

    # Validate count parameter
    count = request.args.get('count', type=int)
    if not count or count <= 0:
        return ResponseHelper.default_response("Invalid count. Must be a positive integer.", 400)

    # Get all IoT devices
    devices = IoTDevice.query.all()
    if not devices:
        return ResponseHelper.default_response("No IoT devices found in the database.", 404)

    observations = []
    for device in devices:
        for _ in range(count):
            observation = Observation(
                observationID=f"obs-{datetime.utcnow().timestamp()}-{random.randint(1000, 9999)}",
                timestamp=datetime.utcnow() - timedelta(minutes=random.randint(0, 1440)),
                temperature=round(random.uniform(-10, 40), 2),
                humidity=round(random.uniform(0, 100), 2),
                windSpeed=round(random.uniform(0, 20), 2),
                precipitation=round(random.uniform(0, 10), 2),
                locationCoordinates=f"{round(random.uniform(-90, 90), 6)}, {round(random.uniform(-180, 180), 6)}",
                deviceID=device.deviceID
            )
            observations.append(observation)

    db.session.add_all(observations)
    db.session.commit()

    return ResponseHelper.default_response(
        "Mock observations generated successfully.",
        201,
        {"generatedObservations": len(observations)}
    )
