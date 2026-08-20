from flask import jsonify

def make_response(data=None, message="Success", status_code=200):
    return jsonify({
        "success": True,
        "message": message,
        "data": data
    }), status_code

def make_error(message="An error occurred", status_code=400, details=None):
    return jsonify({
        "success": False,
        "error": message,
        "details": details
    }), status_code
