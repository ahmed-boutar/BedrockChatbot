import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from config import Config

logger = logging.getLogger(__name__)

class ConversationManager:
    def __init__(self):
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}
        self.session_timestamps: Dict[str, datetime] = {}
        self.max_history = Config.MAX_CONVERSATION_HISTORY
        self.timeout = timedelta(seconds=Config.CONVERSATION_TIMEOUT)
        logger.info("Conversation manager initialized")
    
    def add_message(self, session_id: str, role: str, content: str):
        """Add a message to the conversation history"""
        try:
            # Clean up expired sessions
            self._cleanup_expired_sessions()
            
            if session_id not in self.conversations:
                self.conversations[session_id] = []
            
            message = {
                "role": role,
                "content": content,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            self.conversations[session_id].append(message)
            self.session_timestamps[session_id] = datetime.utcnow()
            
            # Keep only the last N messages to prevent memory issues
            if len(self.conversations[session_id]) > self.max_history:
                self.conversations[session_id] = self.conversations[session_id][-self.max_history:]
            
            logger.info(f"Added {role} message to session {session_id}")
            
        except Exception as e:
            logger.error(f"Error adding message to conversation: {str(e)}")
            raise
    
    def get_context(self, session_id: str) -> List[Dict[str, Any]]:
        """Get conversation context for AI model"""
        try:
            if session_id not in self.conversations:
                return []
            
            # Return conversation history without timestamps for AI context
            context = []
            for msg in self.conversations[session_id]:
                context.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
            
            return context
            
        except Exception as e:
            logger.error(f"Error getting context: {str(e)}")
            return []
    
    def get_conversation_history(self, session_id: str) -> List[Dict[str, Any]]:
        """Get full conversation history including timestamps"""
        try:
            return self.conversations.get(session_id, [])
        except Exception as e:
            logger.error(f"Error getting conversation history: {str(e)}")
            return []
    
    def clear_conversation(self, session_id: str):
        """Clear conversation history for a session"""
        try:
            if session_id in self.conversations:
                del self.conversations[session_id]
            if session_id in self.session_timestamps:
                del self.session_timestamps[session_id]
            
            logger.info(f"Cleared conversation for session {session_id}")
            
        except Exception as e:
            logger.error(f"Error clearing conversation: {str(e)}")
            raise
    
    def get_active_sessions(self) -> List[str]:
        """Get list of active session IDs"""
        try:
            self._cleanup_expired_sessions()
            return list(self.conversations.keys())
        except Exception as e:
            logger.error(f"Error getting active sessions: {str(e)}")
            return []
    
    def _cleanup_expired_sessions(self):
        """Remove expired conversation sessions"""
        try:
            current_time = datetime.utcnow()
            expired_sessions = []
            
            for session_id, timestamp in self.session_timestamps.items():
                if current_time - timestamp > self.timeout:
                    expired_sessions.append(session_id)
            
            for session_id in expired_sessions:
                if session_id in self.conversations:
                    del self.conversations[session_id]
                del self.session_timestamps[session_id]
                logger.info(f"Cleaned up expired session: {session_id}")
                
        except Exception as e:
            logger.error(f"Error during session cleanup: {str(e)}")