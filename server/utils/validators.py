from flask import Request
from config import Config

def validate_message_request(request: Request) -> str:
    """Validate incoming message request"""
    
    if not request.is_json:
        return "Request must be JSON"
    
    data = request.get_json()
    
    if not data:
        return "Request body cannot be empty"
    
    message = data.get('message', '').strip()
    
    if not message:
        return "Message cannot be empty"
    
    if len(message) > Config.MAX_MESSAGE_LENGTH:
        return f"Message too long. Maximum length is {Config.MAX_MESSAGE_LENGTH} characters"
    
    # Check for session_id if provided
    session_id = data.get('session_id', '')
    if session_id and len(session_id) > 100:
        return "Session ID too long"
    
    return None 