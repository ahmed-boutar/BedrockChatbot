import React, { useEffect, useRef } from 'react';
import { Container, Card, Button, Alert, Spinner } from 'react-bootstrap';
import { ChatMessage } from './ChatMessage';
import { ChatInput } from './ChatInput';
import { useChat } from '../hooks/useChat';
import { ChatDots, Trash } from 'react-bootstrap-icons';

export const ChatContainer: React.FC = () => {
  const { messages, isLoading, error, sendMessage, clearChat } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <Container fluid className="h-100 d-flex align-items-center justify-content-center p-4">
      <Card style={{ width: '100%', maxWidth: '800px', height: '90vh' }} className="shadow-lg">
        {/* Header */}
        <Card.Header className="bg-primary text-white d-flex justify-content-between align-items-center">
          <div className="d-flex align-items-center">
            <ChatDots size={24} className="me-2" />
            <h5 className="mb-0">AI Chatbot</h5>
          </div>
          {messages.length > 0 && (
            <Button
              variant="outline-light"
              size="sm"
              onClick={clearChat}
              className="d-flex align-items-center"
            >
              <Trash size={16} className="me-1" />
              Clear
            </Button>
          )}
        </Card.Header>

        {/* Messages Area */}
        <Card.Body 
          className="d-flex flex-column p-0"
          style={{ height: 'calc(90vh - 140px)', overflow: 'hidden' }}
        >
          <div 
            className="flex-grow-1 p-3"
            style={{ 
              overflowY: 'auto',
              backgroundColor: '#f8f9fa'
            }}
          >
            {messages.length === 0 ? (
              <div className="d-flex align-items-center justify-content-center h-100 text-muted">
                <div className="text-center">
                  <ChatDots size={48} className="mb-3 opacity-50" />
                  <h4>Start a conversation!</h4>
                  <p>Type a message to begin chatting with the AI.</p>
                </div>
              </div>
            ) : (
              <>
                {messages.map((message) => (
                  <ChatMessage key={message.id} message={message} />
                ))}
                {isLoading && (
                  <div className="d-flex mb-3">
                    <div className="flex-shrink-0 me-2">
                      <div 
                        className="rounded-circle d-flex align-items-center justify-content-center"
                        style={{
                          width: '40px',
                          height: '40px',
                          backgroundColor: '#6c757d',
                          color: 'white'
                        }}
                      >
                        <ChatDots size={16} />
                      </div>
                    </div>
                    <Card className="bg-light">
                      <Card.Body className="py-2 px-3">
                        <div className="d-flex align-items-center">
                          <Spinner animation="grow" size="sm" className="me-2" />
                          <span className="text-muted">AI is typing...</span>
                        </div>
                      </Card.Body>
                    </Card>
                  </div>
                )}
                <div ref={messagesEndRef} />
              </>
            )}
          </div>

          {/* Error Display */}
          {error && (
            <Alert variant="danger" className="mx-3 mb-0">
              {error}
            </Alert>
          )}

          {/* Input Area */}
          <ChatInput onSendMessage={sendMessage} disabled={isLoading} />
        </Card.Body>
      </Card>
    </Container>
  );
};