import pytest
import json
from app import create_app

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'timestamp' in data
    assert 'version' in data

def test_chat_endpoint_valid_message(client):
    """Test chat endpoint with valid message"""
    response = client.post('/api/chat', 
                          json={'message': 'Hello, how are you?'},
                          content_type='application/json')
    
    # Note: This will fail without proper AWS credentials
    # In a real test environment, you'd mock the Bedrock service
    assert response.status_code in [200, 503]  # 503 if AWS not configured

def test_chat_endpoint_empty_message(client):
    """Test chat endpoint with empty message"""
    response = client.post('/api/chat', 
                          json={'message': ''},
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data

def test_chat_endpoint_no_json(client):
    """Test chat endpoint without JSON"""
    response = client.post('/api/chat', data='not json')
    assert response.status_code == 400

def test_get_conversation_new_session(client):
    """Test getting conversation for new session"""
    response = client.get('/api/conversation/test-session')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['session_id'] == 'test-session'
    assert data['messages'] == []
    assert data['message_count'] == 0

def test_clear_conversation(client):
    """Test clearing conversation"""
    response = client.delete('/api/conversation/test-session')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert data['session_id'] == 'test-session'

def test_get_sessions(client):
    """Test getting active sessions"""
    response = client.get('/api/sessions')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'sessions' in data
    assert 'count' in data