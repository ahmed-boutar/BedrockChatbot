import pytest
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