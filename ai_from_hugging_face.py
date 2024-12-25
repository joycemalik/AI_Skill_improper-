from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os


load_dotenv()  # Load environment variables from .env
api_key = os.getenv('API_KEY')


client = InferenceClient(api_key=api_key)

messages = [
	{
		"role": "user",
		"content": "What is the capital of France?"
	}
]

stream = client.chat.completions.create(
    model="mistralai/Mistral-Nemo-Instruct-2407", 
	messages=messages, 
	max_tokens=500,
	stream=True
)

for chunk in stream:
    print(chunk.choices[0].delta.content, end="")