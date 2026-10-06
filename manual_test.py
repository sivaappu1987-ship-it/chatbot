"""Quick manual test of the chatbot"""
from app import app
import json

client = app.test_client()

print("Testing chatbot...")
response = client.post('/api/chat', 
                      json={'message': 'Hello, what is 2+2?'},
                      content_type='application/json')

print(f"Status: {response.status_code}")
data = json.loads(response.data)

if 'response' in data:
    print(f"✓ SUCCESS! Got response: {data['response'][:200]}")
elif 'error' in data:
    print(f"✗ Error: {data['error']}")
else:
    print(f"✗ Unexpected response: {data}")
