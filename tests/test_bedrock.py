import boto3
import json

bedrock = boto3.client("bedrock-runtime")

def generate_response(context):
    try:
        input_data = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                    {
                        "text": "Hello, how are you?",
                    }
                    ]
                }
            ]
        }

        response = bedrock.invoke_model(
            modelId='amazon.nova-micro-v1:0',
            body=json.dumps(input_data),
            accept='application/json',
            contentType='application/json'
        )
        
        response_body = response['body'].read().decode('utf-8')
        response_data = json.loads(response_body)
        content_list = response_data.get('output', {}).get('message', {}).get('content', [])
        formatted_response = "\n".join([item.get('text', '') for item in content_list])
        return formatted_response.strip() if formatted_response else "No response from model."
        
    except Exception as e:
        return f"Error: {str(e)}"

# Correct input format
print(generate_response("hello"))
