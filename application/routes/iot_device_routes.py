from flask import Blueprint, request
from application.models import IoTDevice, db
from application.utils import ResponseHelper
import uuid

iot_device_bp = Blueprint('iot_device', __name__, url_prefix='/iot-devices')

# Create IoT Device
@iot_device_bp.route('/', methods=['POST'])
def create_device():
    """Register a new IoT device."""
    data = request.get_json()
    location = data.get('location')
    battery_status = data.get('batteryStatus')
    transmission_interval = data.get('transmissionInterval')

    if not location or not battery_status or not transmission_interval:
        return ResponseHelper.default_response("All fields are required", 400)

    # Create the IoT device
    device = IoTDevice(
        deviceID=str(uuid.uuid4()),
        location=location,
        batteryStatus=battery_status,
        transmissionInterval=transmission_interval
    )
    db.session.add(device)
    db.session.commit()

    return ResponseHelper.default_response(
        "IoT Device created successfully",
        201,
        {"deviceID": device.deviceID}
    )

# Get All IoT Devices
@iot_device_bp.route('/', methods=['GET'])
def get_devices():
    """Retrieve all IoT devices."""
    devices = IoTDevice.query.all()
    data = [
        {
            "deviceID": device.deviceID,
            "location": device.location,
            "batteryStatus": device.batteryStatus,
            "transmissionInterval": device.transmissionInterval
        }
        for device in devices
    ]

    return ResponseHelper.default_response(
        "IoT Devices retrieved successfully",
        200,
        {"devices": data}
    )

# Get IoT Device by ID
@iot_device_bp.route('/<string:device_id>', methods=['GET'])
def get_device(device_id):
    """Retrieve IoT device details by ID."""
    device = IoTDevice.query.filter_by(deviceID=device_id).first()

    if not device:
        return ResponseHelper.default_response("IoT Device not found", 404)

    data = {
        "deviceID": device.deviceID,
        "location": device.location,
        "batteryStatus": device.batteryStatus,
        "transmissionInterval": device.transmissionInterval
    }

    return ResponseHelper.default_response(
        "IoT Device details retrieved successfully",
        200,
        data
    )
