import json
from datetime import datetime

# Mock IoT Device Registration
def register_device(test_client):
    device_data = {
        "location": "Test Location",
        "batteryStatus": "Full",
        "transmissionInterval": 30
    }
    response = test_client.post("/iot-devices/", json=device_data)
    assert response.status_code == 201
    
    response_data = json.loads(response.data)
    device_id = response_data["data"]["deviceID"]
    
    # Optionally, print the response if needed for debugging
    print("Register Device Response:", response_data)
    
    return device_id, response
    
    # return json.loads(response.data)["data"]["deviceID"]

# Test Adding an Observation
def test_add_observation_success(test_client):
    # Register a mock IoT device
    device_id, device_response = register_device(test_client)
    
    assert device_response.status_code == 201
    device_response_data = json.loads(device_response.data)
    assert "deviceID" in device_response_data["data"]
    print("Device Registered with ID:", device_id)


    # Mock observation data
    observation_data = {
        "deviceID": device_id,
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": 25.3,
        "humidity": 60.5,
        "windSpeed": 5.2,
        "precipitation": 1.5,
        "locationCoordinates": "45.123456, -73.123456"
    }

    # Add observation
    response = test_client.post("/observations/", json=observation_data)
    print("Check resp::::", response)
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert response_data["message"] == "Observation added successfully"
    assert "observationID" in response_data["data"]

# Test Adding an Observation with Invalid Device
def test_add_observation_invalid_device(test_client):
    # Mock observation data with an invalid device ID
    observation_data = {
        "deviceID": "invalid-device-id",
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": 25.3,
        "humidity": 60.5
    }

    # Attempt to add observation
    response = test_client.post("/observations/", json=observation_data)
    assert response.status_code == 404
    response_data = json.loads(response.data)
    assert response_data["message"] == "IoT Device not registered"

# Test Adding an Observation with Missing Fields
def test_add_observation_missing_fields(test_client):
    # Register a mock IoT device
    device_id = register_device(test_client)

    # Mock observation data with missing required fields
    observation_data = {
        "deviceID": device_id,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Attempt to add observation
    response = test_client.post("/observations/", json=observation_data)
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert response_data["message"] == "Validation error: Missing required fields"

# Test Retrieving Observations
def test_get_observations_success(test_client):
    # Register a mock IoT device
    device_id = register_device(test_client)

    # Add a mock observation
    observation_data = {
        "deviceID": device_id,
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": 25.3,
        "humidity": 60.5,
        "windSpeed": 5.2,
        "precipitation": 1.5,
        "locationCoordinates": "45.123456, -73.123456"
    }
    test_client.post("/observations/", json=observation_data)

    # Retrieve observations
    response = test_client.get("/observations/")
    print("Get Res: ", response)
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["message"] == "Observations retrieved successfully"
    assert len(response_data["data"]["observations"]) > 0

# Test Retrieving Observations with Filters
def test_get_observations_with_filters(test_client):
    # Register a mock IoT device
    device_id = register_device(test_client)

    # Add multiple mock observations
    observation_data_1 = {
        "deviceID": device_id,
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": 20.0,
        "humidity": 50.0
    }
    observation_data_2 = {
        "deviceID": device_id,
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": 30.0,
        "humidity": 70.0
    }
    test_client.post("/observations/", json=observation_data_1)
    test_client.post("/observations/", json=observation_data_2)

    # Retrieve observations filtered by deviceID
    response = test_client.get(f"/observations/?deviceID={device_id}")
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert len(response_data["data"]["observations"]) == 2
