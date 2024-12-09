from flask import jsonify

class ResponseHelper:
    @staticmethod
    def default_response(message, status_code, data=None):
        """
        Generate a standardized API response.
        Args:
            message (str): A message to include in the response.
            status_code (int): HTTP status code.
            data (dict, optional): Data to include in the response. Defaults to None.
        Returns:
            Response: A Flask JSON response object.
        """
        response = {
            "message": message,
            "status_code": status_code,
        }
        if data:
            response["data"] = data
        return jsonify(response), status_code
