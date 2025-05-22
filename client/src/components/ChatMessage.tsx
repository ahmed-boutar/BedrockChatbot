import React from 'react';
import { Card, Badge } from 'react-bootstrap';
import { Message } from '../types/chat';
import { PersonFill, ChatDots } from 'react-bootstrap-icons';

interface ChatMessageProps {
  message: Message;
}

export const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.sender === 'user';
  
  return (
    <div className={`d-flex mb-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      <div className={`flex-shrink-0 me-2 ms-2`}>
        <div 
          className={`rounded-circle d-flex align-items-center justify-content-center`}
          style={{
            width: '40px',
            height: '40px',
            backgroundColor: isUser ? '#0d6efd' : '#6c757d',
            color: 'white'
          }}
        >
          {isUser ? <PersonFill size={16} /> : <ChatDots size={16} />}
        </div>
      </div>
      
      <div style={{ maxWidth: '80%' }}>
        <Card className={`${isUser ? 'bg-primary text-white' : 'bg-light'}`}>
          <Card.Body className="py-2 px-3">
            <div style={{ whiteSpace: 'pre-wrap' }}>{message.text}</div>
          </Card.Body>
        </Card>
        <div className={`text-muted small mt-1 ${isUser ? 'text-end' : 'text-start'}`}>
          {message.timestamp.toLocaleTimeString()}
        </div>
      </div>
    </div>
  );
};