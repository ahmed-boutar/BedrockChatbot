import axios from 'axios';
import { ChatResponse } from '../types/chat';

const API_BASE_URL = 'http://localhost:5001/api'; // Adjust to match your Flask backend URL

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const sendMessage = async (message: string, sessionId?: string): Promise<ChatResponse> => {
  try {
    const response = await api.post('/chat', { 
      message,
      session_id: sessionId || 'default'
    });
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      throw new Error(error.response?.data?.error || 'Failed to send message');
    }
    throw new Error('An unexpected error occurred');
  }
};