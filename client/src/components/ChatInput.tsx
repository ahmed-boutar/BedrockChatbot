import React, { useState, KeyboardEvent } from 'react';
import { Form, Button, InputGroup } from 'react-bootstrap';
import { Send } from 'react-bootstrap-icons';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
}

export const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, disabled }) => {
  const [input, setInput] = useState('');

  const handleSend = () => {
    if (input.trim() && !disabled) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="border-top bg-white p-3">
      <InputGroup>
        <Form.Control
          as="textarea"
          value={input}
          onChange={(e: any) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder="Type your message..."
          disabled={disabled}
          rows={1}
          style={{
            resize: 'none',
            minHeight: '40px',
            maxHeight: '120px',
          }}
        />
        <Button
          variant="primary"
          onClick={handleSend}
          disabled={!input.trim() || disabled}
        >
          <Send size={18} />
        </Button>
      </InputGroup>
    </div>
  );
};