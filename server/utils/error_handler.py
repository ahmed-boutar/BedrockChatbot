import logging
from flask import jsonify
from datetime import datetime

logger = logging.getLogger(__name__)

def handle_error(error: Exception):
    """Centralized error handling"""
    error_message = str(error)
    
    # Log the error
    logger.error(f"Application error: {error_message}")
    
    # Determine appropriate HTTP status code and response
    if "AWS" in error_message or "Bedrock" in error_message:
        status_code = 503
        user_message = "AI service is temporarily unavailable. Please try again later."
    elif "validation" in error_message.lower():
        status_code = 400
        user_message = error_message
    elif "not found" in error_message.lower():
        status_code = 404
        user_message = "Requested resource not found."
    else:
        status_code = 500
        user_message = "An internal error occurred. Please try again later."
    
    return jsonify({
        'error': user_message,
        'timestamp': datetime.utcnow().isoformat(),
        'status': status_code
    }), status_code