## Overview

A Flask-based backend service for a conversational AI assistant using Amazon Bedrock.

## Features

- **Conversation Management**: Maintains conversation history and context
- **Memory**: Remembers previous interactions within a session
- **Error Handling**: Comprehensive error handling and logging
- **Session Management**: Multiple conversation sessions support
- **AWS Bedrock Integration**: Uses Amazon Nova Micro model
- **RESTful API**: Clean API design with proper HTTP status codes
- **Testing**: Test suite with coverage reporting

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment**:
   Copy `.env.example` to `.env` and configure your settings:
   ```bash
   cp .env.example .env
   ```
   
   Update the values in `.env` with your AWS credentials and preferences.

3. **AWS Configuration**:
   Ensure your AWS credentials are configured for Bedrock access:
   ```bash
   aws configure
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```

## API Endpoints

### Chat
- **POST** `/api/chat` - Send a message to the AI
- **Body**: `{"message": "Hello", "session_id": "optional"}`

### Conversation Management
- **GET** `/api/conversation/<session_id>` - Get conversation history
- **DELETE** `/api/conversation/<session_id>` - Clear conversation

### Utility
- **GET** `/api/health` - Health check
- **GET** `/api/sessions` - Get active sessions

## Testing

Run tests with coverage:
```bash
python run_tests.py
```

NOTE: Make sure you have created a logs folder under server or the test won't work

## Project Structure

```
client/                 # React app (VITE)
server/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── services/
│   ├── bedrock_service.py    # AWS Bedrock integration
│   └── conversation_manager.py # Conversation management
├── utils/
│   ├── error_handler.py      # Error handling utilities
│   └── validators.py         # Request validation
├── tests/                # Test suite
├── logs/                 # Application logs
└── requirements.txt      # Python dependencies
```

## Environment Variables

- `AWS_REGION`: AWS region for Bedrock (default: us-east-1)
- `BEDROCK_MODEL_ID`: Bedrock model ID (default: amazon.nova-micro-v1:0)
- `MAX_CONVERSATION_HISTORY`: Max messages per session (default: 20)
- `MAX_MESSAGE_LENGTH`: Max message length (default: 4000)
- `CONVERSATION_TIMEOUT`: Session timeout in seconds (default: 3600)