from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import logging
import os
from services.bedrock_service import BedrockService
from services.conversation_manager import ConversationManager
from utils.error_handler import handle_error
from utils.validators import validate_message_request
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:5173", "http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize services
    bedrock_service = BedrockService()
    conversation_manager = ConversationManager()
    
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        })
    
    @app.route('/api/chat', methods=['POST'])
    def chat():
        """Main chat endpoint"""
        try:
            # Validate request
            validation_error = validate_message_request(request)
            if validation_error:
                return jsonify({'error': validation_error}), 400
            
            data = request.get_json()
            user_message = data.get('message', '').strip()
            session_id = data.get('session_id', 'default')
            
            if not user_message:
                return jsonify({'error': 'Message cannot be empty'}), 400
            
            logger.info(f"Received message for session {session_id}: {user_message[:100]}...")
            
            # Add user message to conversation history
            conversation_manager.add_message(session_id, 'user', user_message)
            
            # Get conversation context
            context = conversation_manager.get_context(session_id)
            
            # Generate response using Bedrock
            bot_response = bedrock_service.generate_response(user_message, context)
            
            # Add bot response to conversation history
            conversation_manager.add_message(session_id, 'assistant', bot_response)
            
            logger.info(f"Generated response for session {session_id}: {bot_response[:100]}...")
            
            return jsonify({
                'message': bot_response,
                'session_id': session_id,
                'timestamp': datetime.utcnow().isoformat()
            })
            
        except Exception as e:
            logger.error(f"Error in chat endpoint: {str(e)}")
            return handle_error(e)
    
    @app.route('/api/conversation/<session_id>', methods=['GET'])
    def get_conversation(session_id):
        """Get conversation history for a session"""
        try:
            history = conversation_manager.get_conversation_history(session_id)
            return jsonify({
                'session_id': session_id,
                'messages': history,
                'message_count': len(history)
            })
        except Exception as e:
            logger.error(f"Error getting conversation: {str(e)}")
            return handle_error(e)
    
    @app.route('/api/conversation/<session_id>', methods=['DELETE'])
    def clear_conversation(session_id):
        """Clear conversation history for a session"""
        try:
            conversation_manager.clear_conversation(session_id)
            return jsonify({
                'message': f'Conversation {session_id} cleared successfully',
                'session_id': session_id
            })
        except Exception as e:
            logger.error(f"Error clearing conversation: {str(e)}")
            return handle_error(e)
    
    @app.route('/api/sessions', methods=['GET'])
    def get_sessions():
        """Get all active session IDs"""
        try:
            sessions = conversation_manager.get_active_sessions()
            return jsonify({
                'sessions': sessions,
                'count': len(sessions)
            })
        except Exception as e:
            logger.error(f"Error getting sessions: {str(e)}")
            return handle_error(e)
    
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Endpoint not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {str(error)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)