import boto3
import json
import logging
from typing import List, Dict, Any
from config import Config

logger = logging.getLogger(__name__)

class BedrockService:
    def __init__(self):
        try:
            self.client = boto3.client(
                "bedrock-runtime",
                region_name=Config.AWS_REGION
            )
            self.model_id = Config.BEDROCK_MODEL_ID
            logger.info(f"Bedrock service initialized with model: {self.model_id}")
        except Exception as e:
            logger.error(f"Failed to initialize Bedrock client: {str(e)}")
            raise
    
    def generate_response(self, user_message: str, context: List[Dict[str, Any]] = None) -> str:
        """
        Generate response using Amazon Bedrock
        
        Args:
            user_message: The user's input message
            context: Previous conversation context
            
        Returns:
            Generated response from the AI model
        """
        try:
            # Build messages array with context
            messages = []
            
            # Add conversation history if available
            if context:
                for msg in context[-10:]:  # Last 10 messages for context
                    messages.append({
                        "role": msg["role"],
                        "content": [{"text": msg["content"]}]
                    })
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": [{"text": user_message}]
            })
            
            input_data = {
                "messages": messages,
                "inferenceConfig": {
                    "maxTokens": 1000,
                    "temperature": 0.7,
                    "topP": 0.9
                }
            }
            
            logger.info(f"Sending request to Bedrock with {len(messages)} messages")
            
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(input_data),
                accept='application/json',
                contentType='application/json'
            )
            
            response_body = response['body'].read().decode('utf-8')
            response_data = json.loads(response_body)
            
            # Extract the response text
            content_list = response_data.get('output', {}).get('message', {}).get('content', [])
            formatted_response = "\n".join([item.get('text', '') for item in content_list])
            
            if not formatted_response:
                logger.warning("Empty response from Bedrock model")
                return "I apologize, but I couldn't generate a response at the moment. Please try again."
            
            logger.info(f"Successfully generated response: {formatted_response[:100]}...")
            return formatted_response.strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise Exception(f"Failed to generate AI response: {str(e)}")