import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from services.conversation_manager import ConversationManager

@pytest.fixture
def manager():
    return ConversationManager()

def test_add_message(manager):
    """Test adding messages to conversation"""
    manager.add_message('test-session', 'user', 'Hello')
    history = manager.get_conversation_history('test-session')
    
    assert len(history) == 1
    assert history[0]['role'] == 'user'
    assert history[0]['content'] == 'Hello'
    assert 'timestamp' in history[0]

def test_get_context(manager):
    """Test getting conversation context"""
    manager.add_message('test-session', 'user', 'Hello')
    manager.add_message('test-session', 'assistant', 'Hi there!')
    
    context = manager.get_context('test-session')
    
    assert len(context) == 2
    assert context[0]['role'] == 'user'
    assert context[0]['content'] == 'Hello'
    assert context[1]['role'] == 'assistant'
    assert context[1]['content'] == 'Hi there!'
    assert 'timestamp' not in context[0]  # Context shouldn't include timestamps

def test_clear_conversation(manager):
    """Test clearing conversation"""
    manager.add_message('test-session', 'user', 'Hello')
    manager.clear_conversation('test-session')
    
    history = manager.get_conversation_history('test-session')
    assert len(history) == 0

def test_max_history_limit(manager):
    """Test that conversation history respects max limit"""
    # Add more messages than the limit
    for i in range(25):
        manager.add_message('test-session', 'user', f'Message {i}')
    
    history = manager.get_conversation_history('test-session')
    assert len(history) <= manager.max_history

# New comprehensive tests to cover missing lines

def test_get_conversation_history_empty_session(manager):
    """Test getting history for non-existent session"""
    history = manager.get_conversation_history('non-existent-session')
    assert history == []

def test_get_context_empty_session(manager):
    """Test getting context for non-existent session"""
    context = manager.get_context('non-existent-session')
    assert context == []

def test_clear_conversation_non_existent_session(manager):
    """Test clearing a non-existent conversation"""
    # This should not raise an error
    manager.clear_conversation('non-existent-session')
    history = manager.get_conversation_history('non-existent-session')
    assert history == []

def test_get_active_sessions_empty(manager):
    """Test getting active sessions when none exist"""
    sessions = manager.get_active_sessions()
    assert sessions == []

def test_get_active_sessions_with_data(manager):
    """Test getting active sessions with existing conversations"""
    manager.add_message('session1', 'user', 'Hello')
    manager.add_message('session2', 'user', 'Hi')
    
    sessions = manager.get_active_sessions()
    assert len(sessions) == 2
    assert 'session1' in sessions
    assert 'session2' in sessions

def test_session_timestamps_updated(manager):
    """Test that session timestamps are properly updated"""
    manager.add_message('test-session', 'user', 'Hello')
    assert 'test-session' in manager.session_timestamps
    
    first_timestamp = manager.session_timestamps['test-session']
    
    # Add another message and verify timestamp is updated
    manager.add_message('test-session', 'user', 'Hello again')
    second_timestamp = manager.session_timestamps['test-session']
    
    assert second_timestamp >= first_timestamp

def test_cleanup_expired_sessions(manager):
    """Test cleanup of expired sessions"""
    # Add a message to create a session
    manager.add_message('test-session', 'user', 'Hello')
    
    # Manually set an old timestamp to simulate expiration
    old_time = datetime.utcnow() - timedelta(seconds=manager.timeout.seconds + 100)
    manager.session_timestamps['test-session'] = old_time
    
    # Trigger cleanup by adding a new message
    manager.add_message('new-session', 'user', 'New message')
    
    # The old session should be cleaned up
    assert 'test-session' not in manager.conversations
    assert 'test-session' not in manager.session_timestamps
    assert 'new-session' in manager.conversations

@patch('services.conversation_manager.logger')
def test_add_message_exception_handling(mock_logger, manager):
    """Test exception handling in add_message"""
    # Mock datetime to raise an exception
    with patch('services.conversation_manager.datetime') as mock_datetime:
        mock_datetime.utcnow.side_effect = Exception("Test exception")
        
        with pytest.raises(Exception):
            manager.add_message('test-session', 'user', 'Hello')
        
        mock_logger.error.assert_called()

@patch('services.conversation_manager.logger')
def test_get_conversation_history_exception_handling(mock_logger, manager):
    """Test exception handling in get_conversation_history"""
    # Mock the conversations dict to raise an exception
    with patch.object(manager, 'conversations') as mock_conversations:
        mock_conversations.get.side_effect = Exception("Test exception")
        
        result = manager.get_conversation_history('test-session')
        assert result == []
        mock_logger.error.assert_called()

@patch('services.conversation_manager.logger')
def test_get_active_sessions_exception_handling(mock_logger, manager):
    """Test exception handling in get_active_sessions"""
    # Mock cleanup method to raise an exception
    with patch.object(manager, '_cleanup_expired_sessions') as mock_cleanup:
        mock_cleanup.side_effect = Exception("Test exception")
        
        result = manager.get_active_sessions()
        assert result == []
        mock_logger.error.assert_called()

@patch('services.conversation_manager.logger')
def test_cleanup_expired_sessions_exception_handling(mock_logger, manager):
    """Test exception handling in _cleanup_expired_sessions"""
    # Add a session
    manager.add_message('test-session', 'user', 'Hello')
    
    # Mock datetime to raise an exception during cleanup
    with patch('services.conversation_manager.datetime') as mock_datetime:
        mock_datetime.utcnow.side_effect = Exception("Test exception")
        
        # This should not raise, but should log the error
        manager._cleanup_expired_sessions()
        mock_logger.error.assert_called()

def test_cleanup_expired_sessions_with_mixed_sessions(manager):
    """Test cleanup with both expired and active sessions"""
    current_time = datetime.utcnow()
    
    # Add an active session
    manager.add_message('active-session', 'user', 'Hello')
    
    # Add an expired session by manipulating timestamps
    manager.conversations['expired-session'] = [{'role': 'user', 'content': 'Old message'}]
    manager.session_timestamps['expired-session'] = current_time - timedelta(seconds=manager.timeout.seconds + 100)
    
    # Trigger cleanup
    manager._cleanup_expired_sessions()
    
    # Active session should remain, expired should be gone
    assert 'active-session' in manager.conversations
    assert 'expired-session' not in manager.conversations
    assert 'expired-session' not in manager.session_timestamps

def test_clear_conversation_removes_both_dicts(manager):
    """Test that clear_conversation removes from both conversations and session_timestamps"""
    manager.add_message('test-session', 'user', 'Hello')
    
    # Verify both dicts have the session
    assert 'test-session' in manager.conversations
    assert 'test-session' in manager.session_timestamps
    
    manager.clear_conversation('test-session')
    
    # Verify both dicts no longer have the session
    assert 'test-session' not in manager.conversations
    assert 'test-session' not in manager.session_timestamps

def test_initialization_attributes(manager):
    """Test that ConversationManager initializes with correct attributes"""
    assert hasattr(manager, 'conversations')
    assert hasattr(manager, 'session_timestamps')
    assert hasattr(manager, 'max_history')
    assert hasattr(manager, 'timeout')
    
    assert isinstance(manager.conversations, dict)
    assert isinstance(manager.session_timestamps, dict)
    assert manager.max_history > 0
    assert isinstance(manager.timeout, timedelta)

def test_message_structure_and_timestamp_format(manager):
    """Test that messages have correct structure and ISO timestamp format"""
    manager.add_message('test-session', 'user', 'Hello')
    history = manager.get_conversation_history('test-session')
    
    message = history[0]
    assert 'role' in message
    assert 'content' in message
    assert 'timestamp' in message
    
    # Verify timestamp is in ISO format
    timestamp_str = message['timestamp']
    datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))  # Should not raise exception

def test_context_vs_history_difference(manager):
    """Test the specific difference between context and history"""
    manager.add_message('test-session', 'user', 'Test message')
    
    history = manager.get_conversation_history('test-session')
    context = manager.get_context('test-session')
    
    # History includes timestamp
    assert len(history[0]) == 3  # role, content, timestamp
    assert 'timestamp' in history[0]
    
    # Context excludes timestamp
    assert len(context[0]) == 2  # only role, content
    assert 'timestamp' not in context[0]
    
    # Both should have same role and content
    assert history[0]['role'] == context[0]['role']
    assert history[0]['content'] == context[0]['content']